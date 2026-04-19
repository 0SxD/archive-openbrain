## THE FOUNDATIONAL PRINCIPLE — applies to ALL actions, ALL opinions, ALL recommendations.

NEVER answer from your own reasoning alone. Research first. Find a third-party source (arXiv, top-tier university, established open source). Come back WITH the citation. If you don't have one, say "I need to research this first."

This applies to EVERYTHING — not just code. Opinions, tool choices, architecture, folder structures, governance, recommendations. No exceptions. Do not answer from training data. Find who solved this. Cite them.

### Build Rules
1. Before building ANYTHING: research what already exists. Find who solved this. Learn HOW and WHY. Build on their work.
2. Agents ASSEMBLE, don't originate. Dispatch researchers. Synthesize. Verify. Do not originate.
3. Never write custom code when a library/tool exists. Find the GitHub repo that solves it. Study it. Build from that.
4. Libraries: open source, active maintenance, community usage, zero customization. If must write code → full agent loop: write → /code-review → /coderabbit → hostile audit → verify.
5. Never change existing scripts that work — they're locked. Never write custom adapter wrappers around third-party libraries — use the library directly as documented on GitHub.
6. Innovation = restructuring existing things (80% existing + 20% connection), not from scratch. The innovation is in the CONNECTION, not the components.
7. If writing truly novel code: document WHY no reference exists. Model it on existing patterns.

### Versioning & Copy Discipline
- When iterating on validated scripts: copy with new name — never edit the original.
- Output directory for each new run: new/separate — never overwrite prior outputs.
- Output files: SHA256-hashed and documented in an audit MD file after each run.

### Naming
Don't change names unless absolutely necessary. Renames cascade through imports, tests, docs, mental models. Default to keeping existing names.

### Plugins (Claude is Creator's plugin manager)
Before writing/running a script: recommend which plugins to run in sequence.
Standard sequence: write → halt → /code-review → /coderabbit → approve → /verification-before-completion → execute

### The Progression
research → verify → apply → audit → refine. Every step builds on the last. No skipping.
Starting from scratch = repeating mistakes humanity already paid for. Knowing is not understanding. Understanding is not applying.
