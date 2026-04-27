---
name: beads-evidence-triage
description: Turn raw failures into high-signal beads. USE WHEN logs, repro commands, or observed behavior need to become self-contained evidence-first tasks instead of vague TODOs.
---

# Beads Evidence Triage

Use this skill when the hard part is converting observations into a bead that another agent can execute without archaeology.

Outcome rule:
- facts first
- hypotheses labeled as hypotheses
- acceptance criteria that can disprove the theory

## Workflow

1. Read [references/evidence-bead-template.md](references/evidence-bead-template.md).
2. Extract:
   - exact repro or trigger
   - observed evidence
   - likely fix surface if justified
   - risk or impact
3. Create the bead with:
   - description for the task and why it matters
   - `--context` for files, commands, and current state
   - `--notes` for provenance using `SOURCES:` and `kn entry:`
4. If the work is clearly multi-step, decompose immediately into child beads.

## Anti-patterns

Do not create beads that say only:
- investigate this
- fix later
- flaky maybe

If the evidence is weak, say so explicitly instead of pretending certainty.
