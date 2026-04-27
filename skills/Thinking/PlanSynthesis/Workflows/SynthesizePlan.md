# Synthesize Plan Workflow

Merges outputs from multiple thinking/research capabilities into a structured execution specification.

## Input

The workflow operates on **whatever capability outputs are available in the current conversation context**. It scans for:

| Source | What to extract | Key sections to find |
|--------|----------------|---------------------|
| **FirstPrinciples** | Fundamental truths, HARD/SOFT/ASSUMPTION constraints, hidden constraints, "Test To Validate" methods, gap analysis, implementation path | `## Deconstruction`, `## Constraint Analysis`, `## Reconstruction` |
| **Council** | Convergence areas, remaining disagreements, recommended path, per-agent positions | `### Round 1/2/3`, `### Council Synthesis` |
| **RedTeam** | Steelman (8 pts), counter-argument (8 pts), convergent strengths/weaknesses, weakness categories | `### PHASE 3: Synthesis`, `### PHASE 4: Steelman`, `### PHASE 5: Red Team Verdict` |
| **Research** | External precedent, verified patterns, domain context | Varies by mode (quick/standard/extensive) |
| **IterativeDepth** | Per-lens findings, new/refined ISC criteria, key insight | `🔍 ITERATIVE DEPTH COMPLETE`, `📋 NEW ISC CRITERIA` |
| **BeCreative** | Branch explorations, viability assessments, hybrid solutions, unconventional options | `### Branching Exploration`, `### Hybrid Solution`, `### Viability Assessment` |
| **WorldThreatModel** | Time-horizon scenarios (6mo/1yr/5yr), model updates, predictions | `### 6-Month Horizon`, `### 1-Year Horizon`, `### 5-Year Horizon` |
| **Science** | Hypotheses, experiment designs, validation methods, results, validated/invalidated status | `### Hypotheses`, `### Experiment Design`, `### Results`, `### Analysis` |

If a source wasn't invoked, skip it. The workflow adapts to whatever is available — minimum 2 sources.

## Synthesis Process

### Step 1: Extract Convergent Signals

Scan all available outputs for points where **2+ sources independently reach the same conclusion**. These are high-confidence signals. Record:
- The convergent recommendation
- Which sources support it
- Confidence level (number of independent sources agreeing)

### Step 2: Identify Constraints

From FirstPrinciples and RedTeam outputs, classify every constraint:

| Type | Definition | Example |
|------|-----------|---------|
| **HARD** | Laws of physics, API limits, budget caps | "Cloudflare Workers have 128MB memory limit" |
| **SOFT** | Convention, preference, habit | "We usually use TypeScript" |
| **ASSUMPTION** | Unvalidated belief | "Users won't need offline access" |

If FirstPrinciples/RedTeam weren't invoked, note constraints as UNCLASSIFIED.

### Step 3: Extract Validation Needs

From FP/Challenge's ASSUMPTION table and Science's experiment designs, collect everything that needs proving before it can be treated as fact:
- The assumption or hypothesis
- The validation method ("Test To Validate" from FP/Challenge, "Experiment Design" from Science)
- What changes if invalidated

These become `validate` action steps in the Execution Steps table.

### Step 4: Map Tensions

From Council disagreements and RedTeam counter-arguments, identify unresolved tensions:
- What's contested
- Which agents/perspectives disagree
- What information would resolve it
- Default recommendation if no resolution

### Step 5: Preserve Alternative Approaches

From BeCreative branches, FP/Reconstruct blank-slate options, and any unconventional paths that didn't converge into the main plan:
- The approach and its source
- Viability assessment (if BeCreative provided one)
- Key trade-off vs the convergent plan

These are preserved separately from the execution plan — divergent options shouldn't be compressed into convergence. They're escape hatches if the main plan fails or if constraints change.

### Step 6: Build Execution Steps

Order the convergent recommendations into executable steps. For each:
- State the action (imperative, 8-12 words)
- List dependencies (which steps must complete first)
- Define acceptance criterion (binary testable)
- Assign owner: `agent` (AI can do it) or `human` (requires decision/access)

Include `validate` steps from Step 3. These should appear early (validate before building on assumptions).

### Step 7: Compile Risk Register

From RedTeam flags, Council tensions, WorldThreatModel scenarios, and assumption classifications:
- Risk description
- Time horizon (from WorldThreatModel: Now / 6mo / 1yr / 5yr, or "—" if no horizon data)
- Likelihood (high/medium/low)
- Mitigation or acceptance rationale

## Output Template

Produce this exact structure:

```markdown
# Plan Synthesis: [Title]

**Sources:** [list which capabilities contributed]
**Synthesized:** [timestamp]

## Convergent Signals

| # | Recommendation | Sources | Confidence |
|---|---------------|---------|------------|
| 1 | [recommendation] | FP + Council + Research | High (3/3) |
| 2 | [recommendation] | Council + RedTeam | Medium (2/3) |

## Constraints

| Constraint | Type | Source |
|-----------|------|--------|
| [constraint] | HARD | FirstPrinciples |
| [constraint] | SOFT | Council |
| [constraint] | ASSUMPTION | Research |

## Assumptions Requiring Validation

| # | Assumption | Validation Method | If Invalidated | Source |
|---|-----------|------------------|----------------|--------|
| V1 | [unvalidated belief] | [how to test] | [what changes] | FP/Challenge |
| V2 | [hypothesis] | [experiment design] | [what changes] | Science |

## Execution Steps

| # | Action | Depends On | Acceptance Criterion | Owner |
|---|--------|-----------|---------------------|-------|
| 1 | Validate: [assumption V1] | — | [binary test] | agent |
| 2 | [imperative action] | Step 1 | [binary test] | agent |
| 3 | [imperative action] | — | [binary test] | human |

## Alternative Approaches

Divergent options preserved from BeCreative branches and FP/Reconstruct. Not part of the main plan — escape hatches if constraints change or main path fails.

| # | Approach | Source | Viability | Key Trade-off vs Main Plan |
|---|---------|--------|-----------|---------------------------|
| A1 | [unconventional option] | BeCreative/Branch 2 | [high/medium/low] | [what you gain/lose] |
| A2 | [blank-slate option] | FP/Reconstruct Option B | [high/medium/low] | [what you gain/lose] |

## Risk Register

| Risk | Horizon | Likelihood | Mitigation |
|------|---------|-----------|------------|
| [risk from RedTeam] | Now | High | [mitigation] |
| [scenario from WorldThreatModel] | 6mo | Medium | [mitigation] |
| [long-term risk] | 1yr | Low | [acceptance rationale] |

## Unresolved Tensions

| Tension | Perspectives | Resolving Information | Default If Unresolved |
|---------|-------------|----------------------|----------------------|
| [what's contested] | [who disagrees] | [what would settle it] | [fallback recommendation] |

## Decision Log

Decisions made during synthesis (from Council convergence or FirstPrinciples analysis):
- [decision]: [rationale] (source: [which capability])

## Source Artifacts

Full outputs from each capability are preserved below for audit trail. The synthesis above is a compression — when signal is ambiguous, refer to the originals.

| Source | Artifact |
|--------|----------|
| FirstPrinciples | [permalink or "see above: ## Deconstruction: ..."] |
| Council | [permalink or "see above: ## Council Debate: ..."] |
| RedTeam | [permalink or "see above: ## Red Team Parallel Analysis: ..."] |
| Research | [permalink or "see above: Research findings..."] |
```

## Artifact Persistence

**CRITICAL: The synthesis compresses rich outputs. Individual skill outputs must persist for audit trail.**

Before synthesizing, save each source output to the PRD's work directory:

```
MEMORY/WORK/{slug}/
├── PRD.md
├── fp-deconstruct.md      ← FirstPrinciples output
├── council-debate.md       ← Council transcript
├── redteam-analysis.md     ← RedTeam steelman + verdict
├── research-findings.md    ← Research results
├── creative-branches.md    ← BeCreative branches
└── plan-synthesis.md       ← THIS synthesis output
```

When running inside an Algorithm session, write each capability output to a separate file in the PRD work directory BEFORE invoking PlanSynthesis. The synthesis output's `## Source Artifacts` table links to these files.

When running outside an Algorithm session (standalone), outputs stay inline in conversation and the Source Artifacts table uses "see above" references.

## Integration with Algorithm

This workflow is designed to be invoked in the Algorithm's **BUILD** or **PLAN** phase after thinking capabilities have run. The output can be:

1. **Fed directly into ISC criteria** — each Execution Step's acceptance criterion maps to an ISC
2. **Used as the PLAN section** of the PRD's Context
3. **Handed to the user** for approval before EXECUTE begins
4. **Audited later** — Source Artifacts persist full outputs alongside the synthesis

## Example Invocation

```
Skill("Thinking", "synthesize plan from the FirstPrinciples decomposition, Council debate, and Research findings above")
```

The workflow reads the conversation context — no file paths or structured input needed. It finds the outputs by their characteristic formatting (STEELMAN/COUNTER-ARGUMENT for RedTeam, Round headers for Council, Fundamental Truths for FirstPrinciples, etc.).
