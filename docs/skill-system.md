# Skill System

This repository is a public skill library for agent runtimes that understand the `SKILL.md` convention. The design goal is practical reuse without forcing an agent to load every skill, every subskill, or every reference file into context.

## Loading Model

Agent skills use progressive disclosure:

1. **Catalog metadata** — the runtime discovers each `SKILL.md` and keeps only frontmatter `name` and `description` available for routing.
2. **Activated instructions** — when the user request matches a skill description, the agent reads that skill's `SKILL.md` body.
3. **On-demand resources** — workflows, tools, references, scripts, templates, and assets are read or executed only when the activated skill points to them.

The important operational rule is that a skill library can contain many skills, but the agent should not eagerly load every skill body. Metadata is for selection; bodies and resources are for execution.

Primary references:

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)

## Root Skills And Subskills

This repository includes both root skills and subskills:

- **Root skills** are broad routers, such as `Frontend`, `Utilities`, `Beads`, or `Thinking`.
- **Subskills** are more specific operating guides under a root, such as `Beads/RecoveryAudit`, `Frontend/Impeccable/polish`, `Utilities/n8n/n8n-validation-expert`, or `Utilities/Documents/Pdf`.

Every subskill with its own `SKILL.md` has its own frontmatter name, description, path, and activation contract. The public skill tree intentionally includes these subskills with descriptions because they are the practical units agents should reach for when the user asks for concrete work.

## Authoring Conventions

The public export is organized around the same conventions used by the local `CreateSkill` meta-skill and the public Agent Skills guidance:

- Every skill has a `SKILL.md` file with YAML frontmatter.
- Frontmatter includes `name` and `description`.
- Descriptions say what the skill does and when to use it.
- Large bodies should move detailed material into referenced files instead of forcing all detail into `SKILL.md`.
- File references should be relative to the skill folder.
- Scripts and tools should be reusable resources, not pasted into every instruction body.
- Public skills should avoid local machine paths, credentials, private state, and hidden operational assumptions.

## Current Compliance Posture

The automated audit currently reports:

- `132` public skills
- `21` top-level categories
- `111` subskills
- `0` metadata hard-gate errors
- `0` missing relative links
- `0` local path references
- `0` secret-pattern hits

There are still large-skill warnings in the audit report. Those are not publication blockers. Concrete split recommendations are tracked in [`progressive-disclosure-candidates.md`](progressive-disclosure-candidates.md).

## Practical Agent Use

Use the narrowest skill that fits:

- Use `Beads` when the request is broad repo workflow coordination.
- Use `Beads/RecoveryAudit` when the request is specifically about backup, restore, pull, push, or drift recovery.
- Use `Frontend` when the request is broad UI work.
- Use `Frontend/Impeccable/polish` when the request is specifically a final UI polish pass.
- Use `Utilities/n8n` for broad n8n workflow work.
- Use `Utilities/n8n/n8n-node-configuration` when the task is specifically node parameter configuration.

This keeps context small, avoids conflicting instructions, and preserves the agent's attention for the task itself.
