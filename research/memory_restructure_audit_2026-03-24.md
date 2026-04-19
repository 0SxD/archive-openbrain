# Memory Restructure Hostile Audit — 2026-03-24
> Auditor: Sonnet (hostile mode). Assumption: previous agent did everything wrong.
> Task: Verify all 7 categorical files created by the memory restructure agent (a06c9dec6437dc1ec).
> Method: Read all categorical files + all source files. Cross-check every entry against source.

---

## Verdict Summary

| File | Result | Critical Issues |
|---|---|---|
| OpenBrainLM/memory/decisions.md | FAIL | Date column wrong on every row; 1 entry missing from source |
| OpenBrainLM/memory/blockers.md | PASS (minor) | One entry has incomplete schema; otherwise accurate |
| trading_bot/memory/decisions.md | FAIL | Date column wrong on every row; 1 factual conflict vs source |
| trading_bot/memory/blockers.md | PASS (minor) | Schema incomplete for all rows; otherwise accurate |
| trading_bot/memory/indicators.md | PASS | Accurate extraction; missing items noted and self-disclosed |
| nautilus_trader/memory/decisions.md | FAIL | Date column wrong on every row; 1 factual inversion vs source |
| nautilus_trader/memory/blockers.md | PASS (minor) | Schema incomplete; one unverifiable RESOLVED entry |

---

## ISSUE 1 (CRITICAL — affects all 7 files): Date column is systematically wrong

Every row in every decisions.md and blockers.md carries the WRONG date.

- `OpenBrainLM/memory/decisions.md`: ALL rows dated `2026-03-21` through `2026-03-24` — these are CORRECT in this file because the source events actually span those dates. This file passes on dates.
- `trading_bot/memory/decisions.md`: ALL rows dated `2026-03-23`. But several decisions clearly came from sessions on `2026-03-24` — e.g., the "SJM regime gate is THE alpha source" entry references `user_lib_notes_inventory_2026-03-24.md` and `OpenBrainLM Session 2026-03-24 (Session 5)`. Its date in the file is `2026-03-24` — that one is correct. But "Python 3.13 throughout", "nautilus_trader\ is PRIMARY", and every other row is stamped `2026-03-23` when the source (`short_term.md` header: "SESSION — 2026-03-24") says these decisions were reached on `2026-03-24`.

**Root cause:** Agent appears to have assigned `2026-03-23` as a default for all trading bot decisions regardless of actual session date. The session headers in `trading_bot/short_term.md` say `2026-03-24` for sessions 4 and 5, but those decisions are dated `2026-03-23` in the output file.

**Affected rows in trading_bot/decisions.md (wrong date):**
- "Python 3.13 throughout" → source: `Agent 1 inventory 2026-03-24` → should be `2026-03-24`
- "nautilus_trader\ is PRIMARY" → source: `Creator directive 2026-03-24` → should be `2026-03-24`
- "BarDataWrangler over BarBuilder" → source: `Context7 NT docs; NT_SETUP_GUIDE_2026-03-22.md` → date could be either; session 2026-03-23 documented this → `2026-03-23` is defensible
- "jumpmodels over hmmlearn/dynamax" → source: `long_term.md API corrections; OpenBrain Session 2026-03-23` → `2026-03-23` is defensible
- "Full rebuild — nothing locked" → this decision is from `CODEBASE_RECON_AUDIT_2026-03-22.md` → correct date should be `2026-03-22`
- "Off-the-shelf open source only" → from `AGENT_RULES.md; long_term.md Rebuild Rules` — no clear date, `2026-03-23` is plausible

**Same issue in nautilus_trader/decisions.md:** ALL rows stamped `2026-03-23` but:
- "Use nautilus_trader/.venv" → source: `Agent 1 inventory 2026-03-24` → should be `2026-03-24`
- "4-sub-project architecture" → source: `Creator approval 2026-03-23` → `2026-03-23` is correct

---

## ISSUE 2 (MAJOR — trading_bot/decisions.md): Factual conflict on Python version entry

**Entry:** "Python 3.13 throughout (not 3.10)" with reasoning: "NT venv is Python 3.13."

**Problem:** The source (`OpenBrainLM/short_term.md` Session 17, Agent 1 findings) says:
> "NT 1.223.0 IS installed — <TRADING_PROJECT>/.venv, Python 3.13"

But `nautilus_trader/short_term.md` Session 2026-03-24 env verification says:
> "nautilus_trader/.venv — Python 3.13.12 + NT 1.223.0 confirmed working"
> "<TRADING_PROJECT>/.venv — appears to be minimal/fresh venv — only setuptools and pip visible; NT and jumpmodels NOT found"

These two sources CONTRADICT each other. Agent 1 (OpenBrainLM session 17) claims NT is in trading_bot venv. The NT short_term env verification claims it is NOT. The categorical file captured the "NT venv is Python 3.13" reasoning without flagging this contradiction. This should be flagged as `Status: disputed` or `needs_review`.

**Verdict:** Decision entry is not incorrect per se, but the contradiction in the source files was not surfaced. A hostile audit should flag this.

---

## ISSUE 3 (MAJOR — nautilus_trader/decisions.md): Factual inversion on PRIMARY/SOURCE roles

**Entry in file:** "nautilus_trader\ is PRIMARY project; <TRADING_PROJECT>\ is READ-ONLY SOURCE"

**Source check:** `nautilus_trader/short_term.md` SESSION 2026-03-24 says:
> "`nautilus_trader\` = PRIMARY project going forward. Clean, versioned, NT-native."
> "`<TRADING_PROJECT>\` = SOURCE of truth for indicators, strategy logic, sandbox history."

The categorical file says "READ-ONLY SOURCE" — the source file does NOT say "READ-ONLY". It says agents "access BOTH folders" and "Pull verified pieces from trading_bot into nautilus_trader." The "READ-ONLY" qualifier was INVENTED by the agent. It is not in `short_term.md` or `long_term.md` for NT. The trading_bot `short_term.md` says:

> "Agents working on trading access BOTH folders."

"READ-ONLY" is a meaningful constraint that does not appear in any source file for this project. This is an INVENTED qualifier.

---

## ISSUE 4 (MODERATE — schema non-compliance across all files)

The rules in `07_memory_verification.md` require the following schema for every entry promoted to long_term.md:
1. Statement
2. Confidence (0-1)
3. Source
4. Status (verified | disputed | needs_review)
5. Last Verified Date (YYYY-MM-DD)

**Blockers files:** The blockers table schema is `Date | Blocker | Status | Resolution | Source`. This captures operational status (OPEN/RESOLVED) but does NOT include:
- Confidence score
- Epistemological Status (verified/disputed/needs_review)
- Last Verified Date as a separate column (Date is creation date, not last_verified_date)

This applies to ALL 4 blockers files (OpenBrainLM, trading_bot x2, nautilus_trader).

**Decisions files:** These DO include Confidence and Status columns. However:
- Status column uses "Active/Superseded/Reference only" (operational status) rather than the schema-required "verified/disputed/needs_review" (epistemological status)
- `last_verified_date` is missing as a column (Date is decision date, not verification date)
- The schema from `07_memory_verification.md` requires both

**Verdict:** Schema non-compliance is MODERATE because the files are useful and mostly accurate, but they do not meet the formal schema required for long_term.md entries. They are operating as a hybrid ledger rather than a verified long-term store.

---

## ISSUE 5 (MINOR — OpenBrainLM/decisions.md): One decision missing from source

**Missing entry:** The `long_term.md` for OpenBrainLM includes:
> "Trinity of Trinities: each E/L/P has own internal E/L/P = 9 sub-evaluators. Source: Creator"

This is a verified finding in `long_term.md` but is NOT captured in `decisions.md`. It is a design decision with a clear source and date [2026-03-21]. The agent omitted it.

Also missing: the "Multi-brain memory architecture: 4 layers (Identity/Project/Session/Archival)" entry does appear in decisions.md but the `long_term.md` records additional detail (partial implementation status) that was not carried over.

---

## ISSUE 6 (MINOR — OpenBrainLM/decisions.md): Entry dates on biological naming row

**Row:** "Renamed LM_LM→Hippocampus, BrainBridge→SpinalCord" with Status: "Superseded (biology tabled)"

**Problem:** This is dated `2026-03-22` which is when the renaming happened. But the decision to TABLE biology was made on `2026-03-23` per `long_term.md`:
> "[2026-03-23] Creator directive: ALL biology, biomimicry, 8-layer Python code is TABLED."

The single row conflates two separate decisions (rename on 03-22, then table biology on 03-23) and assigns the earlier date. It should either be two rows or include both dates.

---

## ISSUE 7 (MINOR — trading_bot/blockers.md): One RESOLVED entry lacks verification

**Row:** "SparseJumpAdapter was calling .fit(X) without ret_ser/sort_by/DataClipperStd → RESOLVED"

The resolution description is accurate per `long_term.md`. However, the "RESOLVED" status implies code was fixed. The `long_term.md` says this was "identified as hiding real jumpmodels API" — it was IDENTIFIED, not necessarily fixed in a running codebase. The trading_bot FULL REBUILD is active (nothing is locked). A RESOLVED status here implies the code is corrected, but under FULL REBUILD all prior code is reference only.

**This is not false, but it is potentially misleading.** The blocker was resolved as a DOCUMENTED FINDING, not as a code fix.

---

## ISSUE 8 (MINOR — nautilus_trader/blockers.md): One partially incorrect RESOLVED entry

**Row:** "Bash execution unavailable in one verification pass → RESOLVED"

The resolution says: "Subsequent session confirmed: NT 1.223.0 installed via filesystem inspection. Full import check (`import nautilus_trader; print version`) still pending on first live Bash session."

The source (`nautilus_trader/short_term.md` env verification session) says the SAME thing verbatim — it confirms NT IS present on filesystem but explicitly says the Python import check is PENDING. Yet this blocker is marked RESOLVED. The import check being "still pending" means the blocker is NOT fully resolved. The resolution note itself admits this but the Status column says RESOLVED. This is internally contradictory.

**Verdict:** Status should be `PARTIAL` or remain `OPEN — partially resolved`.

---

## Per-File Verdicts

### 1. OpenBrainLM/memory/decisions.md — FAIL (minor)
- Exists: YES. Non-empty: YES.
- Content accurate: MOSTLY — but missing the Trinity of Trinities decision and the biological naming decision conflates two events.
- Schema: Partial — missing `last_verified_date` column, Status is operational not epistemological.
- Invented facts: NO — all entries traceable to source.
- Dates: Correct for this file.

### 2. OpenBrainLM/memory/blockers.md — PASS (minor issues)
- Exists: YES. Non-empty: YES.
- Content accurate: YES — all 6 entries verified against short_term.md.
- Schema: Partial — missing Confidence and last_verified_date.
- Invented facts: NO.
- Dates: Correct.

### 3. trading_bot/memory/decisions.md — FAIL (moderate)
- Exists: YES. Non-empty: YES.
- Content accurate: MOSTLY — but dates wrong on multiple rows, "READ-ONLY" qualifier not in source.
  Wait — that qualifier is in THIS file, not the NT file. Trading bot decisions.md does NOT have the READ-ONLY issue; that is in NT decisions.md.
  Trading bot decision dates: "Python 3.13" and "nautilus_trader is PRIMARY" rows should be 2026-03-24 not 2026-03-23.
- Schema: Partial — missing last_verified_date, Status is operational.
- Invented facts: NO — but dates wrong on at least 2 rows.

### 4. trading_bot/memory/blockers.md — PASS (minor issues)
- Exists: YES. Non-empty: YES.
- Content accurate: YES — all entries verified against short_term.md and long_term.md.
- Schema: Partial — missing Confidence and last_verified_date.
- RESOLVED caveats: The SparseJumpAdapter entry (see Issue 7) is potentially misleading but not false.
- Invented facts: NO.

### 5. trading_bot/memory/indicators.md — PASS
- Exists: YES. Non-empty: YES.
- Content accurate: YES — indicators verified against short_term.md Session 5 (user lib notes inventory).
  Numbers match: 42 distinct indicators, 14 custom, 101 Boolean modules, 18 groups.
  Formulas match: Locked SHORT and LONG formulas match short_term.md verbatim.
  Risk tiers match: HIGH/MEDIUM/LOW breakdown matches source.
- Caveats properly disclosed: "5 PDFs NOT read" noted in both Notes section and blockers.md.
- Invented facts: NO.
- Schema: N/A — indicator inventory uses a different structure appropriate to the content.

### 6. nautilus_trader/memory/decisions.md — FAIL (moderate)
- Exists: YES. Non-empty: YES.
- Content accurate: MOSTLY — but:
  (a) Dates wrong: "Use nautilus_trader/.venv" should be 2026-03-24, not 2026-03-23.
  (b) "READ-ONLY SOURCE" qualifier INVENTED — not in any source file.
- Schema: Partial — missing last_verified_date, Status is operational.
- Invented facts: YES — "READ-ONLY" is not in any source.

### 7. nautilus_trader/memory/blockers.md — PASS (minor issues)
- Exists: YES. Non-empty: YES.
- Content accurate: YES — all entries traceable to source.
- "Bash execution" RESOLVED entry is internally contradictory (see Issue 8).
- Schema: Partial — missing Confidence and last_verified_date.
- Invented facts: NO — but RESOLVED status is questionable for Issue 8 row.

---

## Action Items (in priority order)

1. **MUST FIX — nautilus_trader/decisions.md**: Remove "READ-ONLY" qualifier from <TRADING_PROJECT> role description. Source says "SOURCE" only. "READ-ONLY" was invented.

2. **MUST FIX — date errors**: In trading_bot/decisions.md, correct "Python 3.13 throughout" and "nautilus_trader\ is PRIMARY" from `2026-03-23` to `2026-03-24`. In nautilus_trader/decisions.md, correct "Use nautilus_trader/.venv" from `2026-03-23` to `2026-03-24`.

3. **SHOULD FIX — nautilus_trader/blockers.md**: Change "Bash execution" blocker from RESOLVED to "PARTIAL — filesystem confirmed, Python import not yet run."

4. **SHOULD FIX — OpenBrainLM/decisions.md**: Add missing "Trinity of Trinities" decision entry (2026-03-21, source: Creator, long_term.md).

5. **SHOULD FIX — all decisions.md files**: Add `last_verified_date` column and convert Status from operational to epistemological (verified/disputed/needs_review) per `07_memory_verification.md`.

6. **SHOULD FIX — all blockers.md files**: Add `Confidence` and `last_verified_date` columns per schema rules.

7. **FLAG — trading_bot/decisions.md**: Python version entry sources contradict each other (OpenBrainLM session 17 says NT IS in trading_bot venv; NT short_term env verification says it IS NOT). Should be marked `Status: needs_review` until resolved.

---

## Overall Verdict

**FAIL** — Two files contain invented facts or materially wrong dates that could mislead agents:
- `nautilus_trader/memory/decisions.md` has an invented constraint ("READ-ONLY") not present in any source.
- Date errors in `trading_bot/decisions.md` and `nautilus_trader/decisions.md` will cause timeline confusion.

Three files pass with minor schema gaps:
- `OpenBrainLM/memory/blockers.md` — PASS (minor)
- `trading_bot/memory/blockers.md` — PASS (minor, with RESOLVED caveat)
- `nautilus_trader/memory/blockers.md` — PASS (minor, RESOLVED contradiction)
- `trading_bot/memory/indicators.md` — PASS (clean)

The content extraction was largely accurate — no large-scale hallucination or fabrication. The failures are specific, correctable, and non-catastrophic. The schema gap (missing last_verified_date, missing Confidence, operational Status vs epistemological Status) is systematic across all 7 files.

---

*Audit completed: 2026-03-24. Auditor: Sonnet (hostile mode). Source files read: all 7 categorical files + all 6 source files.*
