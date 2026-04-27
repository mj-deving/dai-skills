---
name: research
description: Source-grounded research workflow for current facts, technical topics, market scans, literature reviews, and evidence-backed recommendations. Use when the user asks to research, investigate, compare sources, verify claims, summarize a topic from sources, or produce a cited briefing.
---

# Research

Use this skill to turn a broad question into a source-grounded answer with explicit uncertainty.

## Operating Rules

- Use current sources when facts may have changed.
- Prefer primary sources: official docs, standards, papers, filings, source repositories, release notes, and direct data.
- Verify URLs before presenting them.
- Separate sourced facts from inference.
- Do not invent citations, quotes, dates, statistics, or source names.
- Keep scope proportional: use the smallest research pass that can answer the question well.

## Mode Selection

- **Quick research**: 1-3 high-quality sources; use for narrow factual checks or lightweight comparisons.
- **Standard research**: 4-8 sources; use for recommendations, tradeoff analysis, market scans, or implementation choices.
- **Deep investigation**: iterative source gathering; use for ambiguous claims, high-stakes decisions, conflicting evidence, or complex landscapes.
- **Technical research**: prioritize official documentation, changelogs, source code, specs, and reproducible examples.
- **Literature research**: prioritize papers, preprints, citations, author/institution context, and methodology limits.

## Workflow

1. Define the exact question, decision, and desired output.
2. Identify source classes needed to answer it.
3. Gather sources and discard weak or duplicative material.
4. Cross-check important claims against independent evidence.
5. Capture uncertainty, caveats, and known disagreement.
6. Synthesize into a concise answer with links to the sources used.

## Source Quality Heuristics

- **High confidence**: primary source, recent enough for the question, directly supports the claim.
- **Medium confidence**: reputable secondary source, consistent with primary evidence, but indirect.
- **Low confidence**: unsourced summary, unclear provenance, marketing copy, social post, or stale page.

## Output Pattern

For most research tasks, return:

- **Answer**: direct response or recommendation.
- **Evidence**: key source-backed findings.
- **Tradeoffs**: what changes the answer.
- **Uncertainty**: unresolved questions or weak evidence.
- **Sources**: links used, grouped by relevance.

For decisions, end with concrete next steps.
