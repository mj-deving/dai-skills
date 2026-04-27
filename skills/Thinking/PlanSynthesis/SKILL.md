---
name: PlanSynthesis
description: Synthesize multi-agent outputs into a single templated execution spec. Consumes any combination of Thinking sub-skill and Research outputs. USE WHEN synthesize plan, plan synthesis, merge findings, execution spec, combine analysis, synthesize outputs, make a plan from.
---

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/PlanSynthesis/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# Plan Synthesis

Merges outputs from multiple thinking/research capabilities into a single, structured execution specification. Replaces manual synthesis in the Algorithm's EXECUTE phase.

**When to use:** After running 2+ capabilities (FirstPrinciples, Council, RedTeam, Research, IterativeDepth, BeCreative, WorldThreatModel, Science) and needing a unified action plan.

**What it does:**
1. Identifies convergent recommendations across sources
2. Separates hard constraints from soft assumptions
3. Produces ordered execution steps with dependencies and acceptance criteria
4. Flags unresolved tensions requiring human decision

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| Synthesize outputs into execution plan | `Workflows/SynthesizePlan.md` |

## Quick Reference

| Input | Output | Time |
|-------|--------|------|
| 2+ thinking/research outputs (inline or referenced) | Templated execution spec | <30s |
