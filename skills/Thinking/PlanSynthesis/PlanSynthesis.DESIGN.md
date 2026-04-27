# PlanSynthesis — Design Document

**Created:** 2026-03-31
**Status:** Active
**Origin:** Algorithm reflection — "What would a smarter AI have designed?"

## Why This Exists

When Algorithm runs invoke multiple thinking skills (FirstPrinciples, Council, RedTeam, Research), their outputs accumulate as unstructured markdown in the conversation. The EXECUTE phase then manually synthesizes these into an action plan — slow, inconsistent, and lossy. Key signals (constraint classifications, convergence metrics, unresolved tensions) get dropped.

PlanSynthesis replaces manual synthesis with a single workflow that produces a templated execution spec.

## How It Works

```
Skill("Thinking", "synthesize plan from the analysis above")
```

The workflow reads conversation context, identifies outputs from thinking capabilities by their characteristic formatting, and produces a structured spec with 9 sections:

1. **Convergent Signals** — recommendations where 2+ sources independently agree
2. **Constraints** — HARD (physics/limits), SOFT (convention), ASSUMPTION (unvalidated)
3. **Assumptions Requiring Validation** — from FP/Challenge "Test To Validate" + Science experiment designs; maps to `validate` action steps
4. **Execution Steps** — ordered, with dependencies, acceptance criteria, and owner assignment; includes `validate` steps early
5. **Alternative Approaches** — divergent options from BeCreative branches + FP/Reconstruct blank-slate options; preserved as escape hatches, not compressed into convergence
6. **Risk Register** — from RedTeam flags, Council tensions, and WorldThreatModel time-horizon scenarios (Now/6mo/1yr/5yr)
7. **Unresolved Tensions** — contested points with resolving information and defaults
8. **Decision Log** — decisions made during synthesis with rationale and source

## Key Design Decisions

- **Context-reading, not file-based:** The workflow reads inline conversation outputs, not saved files. This keeps it frictionless — no "save to file, then synthesize" step.
- **Adaptive to available sources:** Works with any 2+ capability outputs. Missing sources are skipped, not errored.
- **Constraint classification borrowed from RedTeam:** HARD/SOFT/ASSUMPTION taxonomy from FirstPrinciples/RedTeam integration. If neither was invoked, constraints are UNCLASSIFIED.
- **Validation steps as first-class actions:** FP/Challenge's "Test To Validate" and Science's experiment designs map to `validate` steps in Execution Steps, placed early in the order (validate before building on assumptions).
- **Alternative Approaches preserved, not compressed:** BeCreative branches and FP/Reconstruct blank-slate options are kept as escape hatches. Convergence-only synthesis would lose divergent options that become valuable when constraints change.
- **Time-horizon Risk Register:** WorldThreatModel's 6mo/1yr/5yr scenarios get a `Horizon` column instead of being flattened into a single urgency dimension.
- **Owner column in execution steps:** Explicitly marks whether a step needs human decision/access or can be agent-executed. Prevents the "AI assumes it can do everything" failure mode.
- **Template, not freeform:** Fixed markdown sections ensure downstream consumers (Algorithm ISC generation, PRD writing) can reliably extract data.

## Integration Points

- **Algorithm PLAN phase:** Natural invocation point after thinking capabilities run in BUILD
- **ISC generation:** Each execution step's acceptance criterion maps directly to an ISC
- **PRD Context section:** The full spec can serve as the PLAN subsection

## Known Limitations

- Relies on recognizing capability outputs by formatting patterns — novel or custom-formatted outputs may be missed
- Convergence detection is semantic, not structural — may over-count similar-but-different recommendations
- Synthesis is lossy by design — the Source Artifacts section and file persistence mitigate this but don't eliminate it

## Related

- `Thinking/FirstPrinciples/` — constraint source
- `Thinking/Council/` — convergence + tension source
- `Thinking/RedTeam/` — risk + steelman source
- `Research/` — external precedent source
