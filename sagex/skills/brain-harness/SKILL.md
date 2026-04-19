---
name: brain-harness
description: Full session bootup sequence. Triggered when user asks about accessing memory, putting on the harness, checking the brain, or any similar phrase indicating they want full session initialization. Reads all memory files across all active projects and reports session state before asking what we're working on today.
---

# Brain Harness — Full Bootup Sequence

## Trigger phrases (heuristic — match the intent, not the exact words)
Any of these should trigger this sequence:
- "put on the brain harness" / "put on the harness"
- "put on the brain" / "load the brain"
- "do you have a brain?" / "can you access your brain?"
- "load your memory" / "read your memory"
- "boot up" / "get up to speed" / "get context"
- Anything that sounds like the user wants you to initialize for a session

When in doubt: if the user seems to be asking you to get acquainted with the current state of the workspace, run this sequence.

Execute this sequence completely before responding.

## Step 1 — Read propagation manifest
Read: `<WORKSPACE>\.claude\propagation_manifest.md`
This tells you where all project brain paths and hooks live. If it doesn't exist, note it and continue.

## Step 2 — Read global memory
Read in order:
- `C:\Users\Creator.WORKSTATION\.claude\projects\C--apps-ai\memory\MEMORY.md` (routing table — read this first)
- `C:\Users\Creator.WORKSTATION\.claude\OPEN_BRAIN.md` (cross-project identity, if exists)

## Step 3 — Read OpenBrainLM project brain
Read in order:
- `<WORKSPACE>\OpenBrainLM\memory\short_term.md`
- `<WORKSPACE>\OpenBrainLM\memory\long_term.md`
- `<WORKSPACE>\OpenBrainLM\memory\todos.md`
- `<WORKSPACE>\OpenBrainLM\memory\connections.md`
- `<WORKSPACE>\OpenBrainLM\memory\decisions.md` (if exists)
- `<WORKSPACE>\OpenBrainLM\memory\blockers.md` (if exists)

## Step 4 — Read Trading Bot project brain
Read in order:
- `<WORKSPACE>\<TRADING_PROJECT>\memory\short_term.md`
- `<WORKSPACE>\<TRADING_PROJECT>\memory\long_term.md`
- `<WORKSPACE>\<TRADING_PROJECT>\memory\todos.md` (if exists)
- `<WORKSPACE>\<TRADING_PROJECT>\memory\connections.md`
- `<WORKSPACE>\<TRADING_PROJECT>\memory\decisions.md` (if exists)
- `<WORKSPACE>\<TRADING_PROJECT>\memory\blockers.md` (if exists)
- `<WORKSPACE>\<TRADING_PROJECT>\memory\indicators.md` (if exists)

## Step 5 — Read NautilusTrader project brain
Read in order:
- `<WORKSPACE>\nautilus_trader\memory\short_term.md`
- `<WORKSPACE>\nautilus_trader\memory\long_term.md` (if exists)
- `<WORKSPACE>\nautilus_trader\memory\connections.md` (if exists)
- `<WORKSPACE>\nautilus_trader\memory\decisions.md` (if exists)
- `<WORKSPACE>\nautilus_trader\memory\blockers.md` (if exists)

## Step 6 — Check for active handoff
After reading all memory files, look at `OpenBrainLM/memory/short_term.md` for a section marked `## ⚡ SESSION HANDOFF`. If one exists:
- It contains specific first-action instructions. Follow them EXACTLY and IN ORDER.
- The handoff overrides the generic "What are we building today?" question.
- Exception: if Creator gave you a specific task alongside the harness request (e.g. "load the harness then do X"), hold that task in mind — complete the handoff sequence first, then address the additional task.
- Do NOT ask "What are we building today?" if a handoff exists. The handoff tells you what to do. Follow it.
- Only ask "What are we building today?" if there is NO active handoff AND Creator gave no additional task.

If no active handoff section exists, go straight to Step 7.

## Step 7 — Report session state
Report a concise summary (no more than 10 lines):
- Last session: what was being worked on
- Active blockers: list them (from blockers.md files)
- In-progress tasks: list them
- Pending agents: any that were running

## Step 8 — Ask the single question
After the report (and after any handoff actions are complete), ask exactly:

> "What are we building today?"

Wait for the answer. Write it as the session header in the relevant project's `short_term.md` before doing anything else.

---

## What NOT to do
- Do not start any work before completing steps 1-8
- Do not skip an active handoff — if one exists, follow it before asking the generic question
- Do not ask multiple questions — the single question is "What are we building today?"
- Do not skip memory files — read all of them
- Do not summarize from memory alone — read the actual files
