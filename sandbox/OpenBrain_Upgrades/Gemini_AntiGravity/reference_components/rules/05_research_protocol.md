## Research Protocol

### Research Trigger
When Creator assigns a research corridor ("go research X in [notebook]"), the research loop activates:
1. **ASK for research corridor or assigned sources and stick to them.** If Creator doesn't specify a source, ASK which notebook/source before starting. Default: ASK, never assume.
2. Query the assigned notebook ONLY (1-2 focused questions per query — never bundle). Use `select_notebook` directly with the known slug — do NOT use `list_notebooks` or `search_notebooks` to browse.
3. Find gaps in the response → immediately dispatch follow-up queries on those gaps — WITHIN the same assigned corridor.
4. **Verify claims** — when the notebook makes a specific claim (names a paper, cites a stat, references a tool), go verify it against third-party top-tier sources (arXiv, GitHub, Context7, official docs). Verification outside the corridor is OK. New RESEARCH direction outside the corridor = ASK first.
5. Continue until the question is fully answered or Creator redirects. **Max 5 follow-up rounds per corridor, max 3 parallel research agents.** If you hit the cap, report what you have and ASK before going deeper.
6. Save full research to `research/` folder. Save only decisions/action items to `short_term.md`
7. **Unverifiable claims** → quarantine (flag as unverified in research file), don't act on them, tell Creator

Creator gives DIRECTION. Claude manages the steps. Don't wait for Creator to ask "did you follow up on X?"

### Corridor Defaults (when Creator says nothing)
- ASK before expanding scope to a different notebook
- ASK before querying a notebook you weren't assigned
- ASK before starting a new research direction not covered by the original assignment
- Verification via arXiv/GitHub/Context7 = always OK (that's verification, not new research)

### Source Hierarchy
arXiv → top-tier universities (MIT, Stanford, CMU, Berkeley, Oxford) → Google/NVIDIA/institutional open source → battle-tested GitHub repos

### 3 Valid Search Paths
A. paper + connected or unconnected repo
B. GitHub directly (practical/implementation domains)
C. paper alone (theoretical domains)

### Banned Sources
Blog posts | Medium | Stack Overflow | random tutorials
YouTube: acceptable for finding WHO to research — then go to their papers/repos.

### NotebookLM Query Strategy
- Limit to 1-2 questions per query — response window is limited
- More questions = compressed answers. Fewer questions = richer answers.
- Use same session_id for follow-ups (builds context)
- Parallel agents asking different questions = fine (separate queries)
- Never ask "tell me about X, Y, Z, and W" in one query — split into 2-3

### Research Corridor (all auto-research is quarantined)
1. All auto-research outputs → quarantine first (notebook 3e824578)
2. Source criteria are the gate: arXiv, peer-reviewed, top-tier university, open source audited
3. hostile-twin verifies each claim
4. meta-auditor cross-references against existing NotebookLMs
5. Only VERIFIED findings get ingested into main corpus
6. Unverified = blocked. No exceptions.
7. If research leads outside the assigned corridor → ASK Creator before expanding scope

### The Loop
research → notebook check → verify with live sources (Context7, PyPI, GitHub, arXiv) → if wrong, REDO EVERYTHING from step 1.
Don't try to patch — redo from verified ground. This is not a bug in the process. This IS the process.

### Freshness
If source >1 month old: mandatory fresh search before trusting.
