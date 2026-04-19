#!/usr/bin/env python3
"""
PreToolUse Research Gate — Deterministic Pre-Action Authorization
=================================================================
Intercepts Write|Edit tool calls on code files (.py) and blocks execution
unless research evidence exists in the project.

Architecture: Zero-Trust Pre-Tool Hook (Open Agent Passport pattern)
- Exit 0 = allow (research present OR file exempt)
- Exit 2 = block (no research evidence, agent must spawn Scout)

Source: OAP specification, Orchestral AI framework, destructive_command_guard pattern.
The gap between what agents CAN do and what they SHOULD do is an authorization problem,
not an alignment or prompting problem.

Stdin: JSON payload from Claude Code PreToolUse event
  {"tool_name": "Write", "tool_input": {"file_path": "...", "content": "..."}}

Stdout (on block): Actionable denial message injected into agent context
Exit code 2 (on block): Hard blocking error — mechanically prevents file write
"""

import json
import sys
import os
import glob
import time
import re
import subprocess
from datetime import datetime, timezone
from urllib.parse import urlparse

# --- Configuration ---

# Approved source domains for citation URLs in research.md
APPROVED_DOMAINS = [
    'arxiv.org',
    'github.com',
    'docs.nautilustrader.io',
    'scikit-learn.org',
    'feature-engine.trainindata.com',
    'mlflow.org',
    'pypi.org',
    'readthedocs.io',
    'docs.python.org',
]

# File extensions that require research evidence before writing
GATED_EXTENSIONS = {'.py'}

# Paths that are ALWAYS exempt (memory, config, docs, research output)
EXEMPT_PATH_PATTERNS = [
    '/memory/',
    '/.claude/',
    '/.gemini/',
    '/research/',
    '/docs/',
    '/agent_sync/',
    '/logs/',
    '/_backups/',
    '/_archive',
    '/node_modules/',
    '/__pycache__/',
]

# Exempt filenames (regardless of path)
EXEMPT_FILENAMES = [
    'CLAUDE.md', 'GEMINI.md', 'AGENTS.md', 'README.md',
    'OPEN_BRAIN.md', 'MEMORY.md', '.gitignore',
    'settings.json', 'settings.local.json',
    'plugin.json', 'package.json',
]

# Research evidence locations (checked in order)
# Research is "present" if ANY of these contain >50 chars of content
# IMPORTANT: Do NOT add memory files here — they are always fresh and
# would defeat the gate entirely. Only explicit research output counts.
RESEARCH_EVIDENCE_PATHS = [
    'research.md',                    # Project-root research file (primary)
]

# Max age of research evidence in seconds (1 hour)
RESEARCH_MAX_AGE_SECONDS = 3600


def is_exempt_path(file_path: str) -> bool:
    """Check if file path is exempt from the research gate."""
    normalized = file_path.replace('\\', '/')

    # Check exempt path patterns
    for pattern in EXEMPT_PATH_PATTERNS:
        if pattern in normalized:
            return True

    # Check exempt filenames
    basename = os.path.basename(normalized)
    if basename in EXEMPT_FILENAMES:
        return True

    return False


def is_gated_extension(file_path: str) -> bool:
    """Check if the file extension requires research evidence."""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in GATED_EXTENSIONS


def resolve_project_root(target_file_path: str) -> str:
    """
    Fix 1 — Cross-cwd bug: resolve project root from the TARGET file's location,
    not from os.getcwd(). Prevents false-block when editing a file in a different
    project from the current working directory.

    Strategy (in order):
    1. Run `git rev-parse --show-toplevel` from the target file's directory.
    2. Walk up from the target file's directory looking for .git/ or CLAUDE.md.
    3. Fall back to os.getcwd() only if no project root found.
    """
    target_dir = os.path.dirname(os.path.abspath(target_file_path))

    # Strategy 1: git rev-parse
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            root = result.stdout.strip()
            if root:
                return root
    except Exception:
        pass

    # Strategy 2: walk up looking for .git/ or CLAUDE.md
    current = target_dir
    while True:
        if os.path.isdir(os.path.join(current, '.git')) or \
                os.path.isfile(os.path.join(current, 'CLAUDE.md')):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            # Reached filesystem root without finding a marker
            break
        current = parent

    # Strategy 3: fall back to cwd
    return os.getcwd()


def find_research_evidence(target_file_path: str) -> tuple[bool, str, str]:
    """
    Check if research evidence exists in the project.
    Returns (found: bool, location: str, first_url: str).

    Fix 1 — Cross-cwd bug: accepts target_file_path so the correct project
    root is derived from the file being written, not the shell's cwd.

    Fix 2 — Citation quality: research.md must contain at least one URL
    (https?://...) — size > 50 alone is no longer sufficient.

    ONLY checks research.md at project root.
    Does NOT check research/ directory (old files false-positive).
    Does NOT check memory/short_term.md (always fresh, defeats the gate).

    The agent must explicitly create research.md with findings from a
    Scout agent before the gate opens. This is the intentional friction.
    """
    now = time.time()

    # Fix 1: derive project root from the target file, not cwd
    # PROJECT_ROOT env variable removed — resolve_project_root() handles cross-cwd
    # correctly via git, making the env override a redundant bypass vector.
    project_root = resolve_project_root(target_file_path)
    root_candidates = [project_root]

    url_pattern = re.compile(r'https?://\S+')

    def _is_approved_url(url: str) -> bool:
        """Return True if url's domain matches any entry in APPROVED_DOMAINS."""
        try:
            hostname = urlparse(url).hostname or ''
        except Exception:
            return False
        return any(hostname == d or hostname.endswith('.' + d) for d in APPROVED_DOMAINS)

    for root_candidate in root_candidates:
        research_file = os.path.join(root_candidate, 'research.md')
        if os.path.isfile(research_file):
            mtime = os.path.getmtime(research_file)
            age = now - mtime
            if age >= RESEARCH_MAX_AGE_SECONDS:
                continue
            with open(research_file, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            # Require at least one URL from an approved domain
            urls = url_pattern.findall(content)
            if not urls:
                # File exists and is fresh but has no citations
                return False, research_file, ''
            approved = [u for u in urls if _is_approved_url(u)]
            if approved:
                return True, research_file, approved[0]
            # URLs present but none from an approved domain
            return False, research_file, urls[0]

    return False, '', ''


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # Can't parse input — allow (don't block on hook failure)
        sys.exit(0)

    tool_name = payload.get('tool_name', '')

    # Only gate Write and Edit tools
    if tool_name not in ('Write', 'Edit'):
        sys.exit(0)

    # Extract file path from tool input
    tool_input = payload.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        sys.exit(0)

    # Check exemptions
    if is_exempt_path(file_path):
        sys.exit(0)

    if not is_gated_extension(file_path):
        sys.exit(0)

    # --- RESEARCH GATE ---
    # This is a code file. Check for research evidence.
    # Fix 1: pass file_path so find_research_evidence() resolves the correct project root
    found, location, first_url = find_research_evidence(file_path)

    if found:
        # Fix 3 — Citation logging: append a log line when the gate PASSES
        # so there is an auditable record of every approved write.
        try:
            project_root = resolve_project_root(file_path)
            log_path = os.path.join(project_root, '.claude', 'research_citations.log')
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            iso_ts = datetime.now(timezone.utc).isoformat()
            log_line = f"{iso_ts}\t{file_path}\t{location}\t{first_url}\n"
            with open(log_path, 'a', encoding='utf-8') as log_fh:
                log_fh.write(log_line)
        except Exception:
            pass  # Citation log failure must never block the write

        # Research exists — allow the write
        sys.exit(0)
    else:
        # NO research evidence — BLOCK
        # Fix 2 detail: distinguish "no research.md" from "research.md has no citations"
        if location:
            # Distinguish: no URLs at all vs URLs present but none from approved domains
            url_pattern_check = re.compile(r'https?://\S+')
            try:
                with open(location, 'r', encoding='utf-8', errors='replace') as _fh:
                    _content = _fh.read()
                _urls = url_pattern_check.findall(_content)
            except Exception:
                _urls = []

            approved_list = ', '.join(APPROVED_DOMAINS)
            if _urls:
                no_citation_note = (
                    f"research.md exists at {location} but contains no citations from "
                    f"approved domains.\n"
                    f"Approved domains: {approved_list}\n"
                    "Add at least one URL from an approved domain.\n\n"
                )
            else:
                no_citation_note = (
                    f"research.md exists at {location} but contains no citations (URLs).\n"
                    f"Add at least one https:// URL from an approved domain.\n"
                    f"Approved domains: {approved_list}\n\n"
                )
        else:
            no_citation_note = ""

        # Fix 4 — Denial message: corrected to say only research.md at project root
        # is checked (not "research/ directory" which is no longer true).
        denial = (
            "ACCESS DENIED: Research Gate Blocked This Write\n"
            "================================================\n"
            f"Target: {file_path}\n\n"
            + no_citation_note +
            "You are attempting to write a code file without verified research "
            "evidence in your project. This is a deterministic block — you cannot "
            "rationalize past it.\n\n"
            "TO UNBLOCK:\n"
            "1. Spawn a read-only Scout agent to retrieve official documentation\n"
            "2. Save research findings (including at least one citation URL) to research.md\n"
            "   at the project root\n"
            "3. Then retry your write — the gate will check again\n\n"
            "Research evidence must be:\n"
            "- research.md at the project root\n"
            "- Contains at least one citation URL (https://...)\n"
            "- Modified within the last hour\n\n"
            "This hook exists because agents optimize for task completion and "
            "rationalize past text-based rules. This gate is structural, not behavioral."
        )
        print(denial)
        sys.exit(2)


if __name__ == '__main__':
    main()
