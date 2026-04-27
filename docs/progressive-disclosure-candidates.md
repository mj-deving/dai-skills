# Progressive Disclosure Candidates

The publication audit has no hard-gate failures. It does report large `SKILL.md` files that are good candidates for future progressive-disclosure refactors.

The goal is not to remove useful detail. The goal is to keep each activation path cheap:

1. keep `SKILL.md` as the routing and execution entrypoint
2. move detailed command catalogs, examples, provider matrices, and error catalogs into referenced files
3. keep deterministic logic in scripts or tools instead of prose
4. make each reference file directly linked from `SKILL.md`
5. ensure the first activation loads only the minimum needed to choose the next file or tool

## Recommended Refactors

| Skill | Lines | Suggested split | Rationale |
|---|---:|---|---|
| `Utilities/n8n/n8n-mcp-tools-expert/SKILL.md` | 877 | Keep tool-selection rules in `SKILL.md`. Move MCP tool catalog, parameter formats, template operations, credential operations, and workflow-management examples into direct references. | n8n MCP work is broad. Most requests need one tool family, not the entire catalog. |
| `Utilities/n8n/n8n-node-configuration/SKILL.md` | 835 | Keep the node-configuration decision tree in `SKILL.md`. Move operation-specific field rules, display-option behavior, node examples, and patch-vs-full-update guidance into references. | Node configuration is highly conditional. Loading all operation examples up front is expensive. |
| `Utilities/n8n/n8n-code-javascript/SKILL.md` | 784 | Keep Code node mode selection and critical syntax rules in `SKILL.md`. Move item access, HTTP helper patterns, date handling, paired-item behavior, batching, and error recipes into references. | JavaScript Code node tasks vary widely; most require one or two pattern files. |
| `Utilities/n8n/n8n-code-python/SKILL.md` | 774 | Keep the “use Python only when appropriate” rule and mode selection in `SKILL.md`. Move standard-library notes, data access examples, limitations, and error patterns into references. | Python is a narrower path; the full body should not load unless Python is actually requested. |
| `Utilities/n8n/n8n-validation-expert/SKILL.md` | 761 | Keep validation-loop rules in `SKILL.md`. Move error catalog, warning triage, false-positive handling, and auto-fix examples into references. | Validation tasks usually start from a specific error or warning. Reference lookup should be targeted. |
| `Utilities/Documents/Pptx/SKILL.md` | 585 | Keep presentation workflow routing in `SKILL.md`. Move slide layout rules, speaker-note handling, extraction/conversion paths, visual design guidance, and library/API details into references. | PPTX work spans creation, editing, extraction, and conversion. Those paths should not share one large activation body. |
| `Security/Recon/SKILL.md` | 514 | Keep authorization, passive-vs-active mode selection, and safety gates in `SKILL.md`. Move subdomain enumeration, DNS/WHOIS/ASN lookup, JS endpoint discovery, CIDR scanning, and path discovery into references. | Recon has safety-sensitive routing plus many technical techniques. The safety gates should load first; technique detail should load second. |
| `Utilities/n8n/n8n-expression-syntax/SKILL.md` | 525 | Keep the expression syntax quick rules in `SKILL.md`. Move `$json`, `$node`, webhook data, item linking, and common syntax-error recipes into references. | Most expression fixes are narrow and should load the matching pattern only. |
| `Utilities/n8n/n8n-workflow-patterns/SKILL.md` | 512 | Keep architecture-pattern selection in `SKILL.md`. Move webhook, HTTP API, database, AI agent, scheduled, and batch-processing patterns into direct reference files. | Workflow architecture naturally decomposes by pattern type. |

## Suggested Priority

1. n8n specialist skills — several related large files can share one consistent split pattern.
2. `Security/Recon/SKILL.md` — split safety gates from technique catalogs.
3. `Utilities/Documents/Pptx/SKILL.md` — split by document operation mode.

## Completed Refactors

| Skill | Before | After | Notes |
|---|---:|---:|---|
| `graphify/SKILL.md` | 1329 lines | 72 lines | Converted into a router with direct root-level references for setup/detection, extraction, graph outputs, incremental operations, query operations, automation operations, and honesty rules. |

## Acceptance Criteria

A refactor is complete when:

- `SKILL.md` remains sufficient to decide what to do next
- detailed files are linked directly from `SKILL.md`
- no reference is hidden behind deep navigation
- the audit still reports no metadata errors, missing relative links, local paths, or secret-pattern hits
- line-count warnings decrease without deleting useful operational content

## Non-Goals

- Do not flatten all subskills into root skills.
- Do not delete detailed examples just to reduce line counts.
- Do not split files so aggressively that the agent has to chase many small fragments.
- Do not introduce private paths, local machine assumptions, or provider-shaped fake secrets while creating examples.
