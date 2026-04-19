#!/usr/bin/env python3
"""
Destructive Command Guard (Dcg) — PreToolUse Bash Interceptor
==============================================================
Intercepts Bash tool calls and blocks destructive commands that are
hard to reverse, affect shared systems, or could cause data loss.

Architecture: Zero-Trust Pre-Action Authorization
- Exit 0 = allow (command is safe or not matched)
- Exit 2 = block (destructive command detected, safer alternative suggested)

Source: Dcg pattern (destructive_command_guard), OAP specification.
Agents optimize for task completion and will use destructive shortcuts
to bypass obstacles. This gate makes that mechanically impossible.

Stdin: JSON payload from Claude Code PreToolUse event
  {"tool_name": "Bash", "tool_input": {"command": "..."}}
"""

import json
import sys
import re

# --- Destructive Command Patterns ---
# Each entry: (regex_pattern, description, safer_alternative)

DESTRUCTIVE_PATTERNS = [
    # File deletion
    (r'\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--recursive\s+--force|-[a-zA-Z]*f[a-zA-Z]*r)\b',
     'Recursive force delete (rm -rf)',
     'Use rm without -f to get prompts, or move files to a _trash/ directory first'),

    (r'\brm\s+-[a-zA-Z]*f\b.*\*',
     'Force delete with wildcard',
     'List files first with ls, then delete specific files without -f'),

    # Git destructive operations
    (r'\bgit\s+reset\s+--hard\b',
     'git reset --hard (discards all uncommitted changes)',
     'Use git stash to save changes first, or git reset --soft to keep changes staged'),

    (r'\bgit\s+push\s+.*--force\b',
     'git push --force (overwrites remote history)',
     'Use git push --force-with-lease for safer force push, or rebase and push normally'),

    (r'\bgit\s+clean\s+-[a-zA-Z]*f',
     'git clean -f (permanently removes untracked files)',
     'Use git clean -n (dry run) first to see what would be removed'),

    (r'\bgit\s+branch\s+-D\b',
     'git branch -D (force delete branch even if unmerged)',
     'Use git branch -d (lowercase) which warns if branch has unmerged changes'),

    (r'\bgit\s+checkout\s+\.\s*$',
     'git checkout . (discards all unstaged changes)',
     'Use git stash to save changes, or git diff to review what would be lost'),

    (r'\bgit\s+restore\s+\.\s*$',
     'git restore . (discards all unstaged changes)',
     'Use git stash to save changes, or git diff to review what would be lost'),

    # Database destructive operations
    (r'\bDROP\s+(TABLE|DATABASE|SCHEMA|INDEX)\b',
     'DROP statement (permanently deletes database objects)',
     'Use a backup first, or rename/archive instead of dropping'),

    (r'\bTRUNCATE\s+TABLE\b',
     'TRUNCATE TABLE (deletes all rows, cannot be rolled back)',
     'Use DELETE with a WHERE clause, or back up the table first'),

    (r'\bDELETE\s+FROM\s+\w+\s*$',
     'DELETE FROM without WHERE clause (deletes all rows)',
     'Add a WHERE clause to target specific rows'),

    # System destructive operations
    (r'\bkill\s+-9\b',
     'kill -9 (force kill without cleanup)',
     'Use kill (SIGTERM) first to allow graceful shutdown'),

    (r'\bmkfs\b',
     'mkfs (formats a filesystem)',
     'Verify the target device and back up data first'),

    (r'\bdd\s+.*of=/dev/',
     'dd writing to device (can overwrite entire disk)',
     'Double-check the of= target device before proceeding'),

    # Package/dependency destructive
    (r'\bpip\s+uninstall\s+-y\s+',
     'pip uninstall -y (removes packages without confirmation)',
     'Use pip uninstall without -y to get confirmation prompt'),

    (r'\bnpm\s+cache\s+clean\s+--force',
     'npm cache clean --force',
     'Usually unnecessary — npm manages its own cache'),

    # Credential/config exposure
    (r'\bcurl\s+.*(-d|--data).*password',
     'Sending password in curl request body (may be logged)',
     'Use environment variables or a config file for credentials'),
]

# --- File Write Bypass Detection ---
# Catches Bash commands that write to files, bypassing Write/Edit hooks.
# The Write/Edit tools have PreToolUse hooks (research gate, security plugin).
# Bash echo/cat/tee/heredoc bypass those hooks entirely.
# This gate catches the bypass and forces the agent back to Write/Edit.

FILE_WRITE_PATTERNS = [
    # echo/printf redirection to file
    (r'(?:echo|printf)\s+.*>\s*\S+',
     'File write via echo/printf redirection (bypasses Write/Edit hooks)',
     'Use the Write tool instead — it has security hooks that Bash bypasses'),

    # cat heredoc to file
    (r'\bcat\s+>\s*\S+',
     'File write via cat redirection (bypasses Write/Edit hooks)',
     'Use the Write tool instead — it has security hooks that Bash bypasses'),

    # tee to file
    (r'\btee\s+(?!-a).*\S+\.(?:py|js|ts|sh|yml|yaml|json|md)\b',
     'File write via tee (bypasses Write/Edit hooks)',
     'Use the Write tool instead — it has security hooks that Bash bypasses'),

    # cp/mv that could overwrite code files
    # (not blocked — these are legitimate operations, unlike echo > file)

    # python/node one-liner writing files
    (r'python[3]?\s+-c\s+.*(?:open|write).*\.py',
     'Python one-liner writing to .py file (bypasses research gate)',
     'Use the Write tool instead — the research gate checks for evidence before .py writes'),
]

# Exempt patterns — legitimate Bash file operations that should NOT be blocked
FILE_WRITE_EXEMPTIONS = [
    r'>\s*/dev/null',           # Redirect to /dev/null (suppress output)
    r'>\s*&\d',                 # Redirect stderr/stdout merging
    r'2>\s*',                   # stderr redirection only
    r'>\s*\S+\.log\b',         # Log file writes are fine
    r'>\s*\S+\.tmp\b',         # Temp file writes are fine
    r'\|\s*sort\b',            # Piping to sort (not file write)
    r'\bgit\b',                # Git commands that use > for output
]


# Commands that are ALWAYS blocked (no alternative — just don't)
ALWAYS_BLOCKED = [
    (r':(){ :\|:& };:',
     'Fork bomb',
     'This is a denial-of-service attack. Do not run this.'),

    (r'\brm\s+-rf\s+/\s*$',
     'rm -rf / (delete entire filesystem)',
     'This would destroy the entire system. Never run this.'),

    (r'\brm\s+-rf\s+/\*',
     'rm -rf /* (delete entire filesystem contents)',
     'This would destroy the entire system. Never run this.'),

    (r'\b>\s*/dev/sda\b',
     'Writing directly to disk device',
     'This would destroy the disk. Never run this.'),
]


def _is_file_write_exempt(command: str) -> bool:
    """Check if a file-write command matches an exemption pattern."""
    for pattern in FILE_WRITE_EXEMPTIONS:
        if re.search(pattern, command):
            return True
    return False


def check_command(command: str) -> tuple[bool, str, str]:
    """
    Check if a command matches any destructive or bypass pattern.
    Returns (is_blocked, description, alternative).
    """
    # Check always-blocked first
    for pattern, desc, alt in ALWAYS_BLOCKED:
        if re.search(pattern, command):
            return True, desc, alt

    # Check file-write bypass patterns (unless exempt)
    if not _is_file_write_exempt(command):
        for pattern, desc, alt in FILE_WRITE_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True, desc, alt

    # Check destructive patterns
    for pattern, desc, alt in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, desc, alt

    return False, '', ''


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = payload.get('tool_name', '')

    if tool_name != 'Bash':
        sys.exit(0)

    tool_input = payload.get('tool_input', {})
    command = tool_input.get('command', '')

    if not command:
        sys.exit(0)

    is_destructive, description, alternative = check_command(command)

    if is_destructive:
        denial = (
            "DESTRUCTIVE COMMAND GUARD: BLOCKED\n"
            "===================================\n"
            f"Command: {command}\n"
            f"Reason: {description}\n\n"
            f"SAFER ALTERNATIVE: {alternative}\n\n"
            "This is a deterministic block. Destructive commands are intercepted\n"
            "by the Dcg hook before execution. You cannot bypass this gate.\n\n"
            "If you believe this command is necessary, ask Sage for explicit approval.\n"
            "Do NOT attempt to rephrase the command to evade detection."
        )
        print(denial)
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
