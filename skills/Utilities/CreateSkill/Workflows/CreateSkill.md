# CreateSkill Workflow

Create a new skill following the canonical structure with proper TitleCase naming.

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the CreateSkill workflow in the CreateSkill skill to create new skill"}' \
  > /dev/null 2>&1 &
```

Running the **CreateSkill** workflow in the **CreateSkill** skill to create new skill...
-->

## Step 1: Read the Authoritative Sources

**REQUIRED FIRST:**

1. Read the skill system documentation: `${PAI_HOME}/SkillSystem.md`
2. Read the canonical example: `${SKILLS_HOME}/Research/SKILL.md`

## Step 2: Understand the Request

Ask the user:
1. What does this skill do?
2. What should trigger it?
3. What workflows does it need?

## Step 3: Determine TitleCase Names

**All names must use TitleCase (PascalCase).**

| Component | Format | Example |
|-----------|--------|---------|
| Skill directory | TitleCase | `Blogging`, `Daemon`, `CreateSkill` |
| Workflow files | TitleCase.md | `Create.md`, `UpdateDaemonInfo.md` |
| Reference docs | TitleCase.md | `ProsodyGuide.md`, `ApiReference.md` |
| Tool files | TitleCase.ts | `ManageServer.ts` |
| Help files | TitleCase.help.md | `ManageServer.help.md` |

**Wrong naming (NEVER use):**
- `create-skill`, `create_skill`, `CREATESKILL` → Use `CreateSkill`
- `create.md`, `CREATE.md`, `create-info.md` → Use `Create.md`, `CreateInfo.md`

## Step 4: Create the Skill Directory

```bash
mkdir -p ${SKILLS_HOME}/[SkillName]/Workflows
mkdir -p ${SKILLS_HOME}/[SkillName]/Tools
```

**Example:**
```bash
mkdir -p ${SKILLS_HOME}/YourSkill/Workflows
mkdir -p ${SKILLS_HOME}/YourSkill/Tools
```

## Step 5: Create SKILL.md

Follow this exact structure:

```yaml
---
name: SkillName
description: [What it does]. USE WHEN [intent triggers using OR]. [Additional capabilities].
---

# SkillName

[Brief description]

<!-- ## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running WORKFLOWNAME in SKILLNAME"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running **WorkflowName** in **SkillName**...
   ```

**Full documentation:** `${PAI_HOME}/THENOTIFICATIONSYSTEM.md`
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **WorkflowOne** | "trigger phrase" | `Workflows/WorkflowOne.md` |
| **WorkflowTwo** | "another trigger" | `Workflows/WorkflowTwo.md` |

## Examples

**Example 1: [Common use case]**
```
User: "[Typical user request]"
→ Invokes WorkflowOne workflow
→ [What skill does]
→ [What user gets back]
```

**Example 2: [Another use case]**
```
User: "[Different request]"
→ [Process]
→ [Output]
```

## [Additional Documentation]

[Any other relevant info]
```

## Step 6: Create Workflow Files

For each workflow in the routing section:

```bash
touch ${SKILLS_HOME}/[SkillName]/Workflows/[WorkflowName].md
```

### Workflow-to-Tool Integration (REQUIRED for workflows with CLI tools)

**If a workflow calls a CLI tool, it MUST include intent-to-flag mapping tables.**

This pattern translates natural language user requests into appropriate CLI flags:

```markdown
## Intent-to-Flag Mapping

### Model/Mode Selection

| User Says | Flag | When to Use |
|-----------|------|-------------|
| "fast", "quick", "draft" | `--model haiku` | Speed priority |
| (default), "best", "high quality" | `--model opus` | Quality priority |

### Output Options

| User Says | Flag | Effect |
|-----------|------|--------|
| "JSON output" | `--format json` | Machine-readable |
| "detailed" | `--verbose` | Extra information |

## Execute Tool

Based on user request, construct the CLI command:

\`\`\`bash
bun ToolName.ts \
  [FLAGS_FROM_INTENT_MAPPING] \
  --required-param "value"
\`\`\`
```

**Why this matters:**
- Tools have rich configuration via flags
- Workflows should expose this flexibility, not hardcode single patterns
- Users speak naturally; workflows translate to precise CLI

**Reference:** `${PAI_HOME}/CliFirstArchitecture.md` (Workflow-to-Tool Integration section)

**Examples (TitleCase):**
```bash
touch ${SKILLS_HOME}/YourSkill/Workflows/UpdateDaemonInfo.md
touch ${SKILLS_HOME}/YourSkill/Workflows/UpdatePublicRepo.md
touch ${SKILLS_HOME}/YourSkill/Workflows/Create.md
touch ${SKILLS_HOME}/YourSkill/Workflows/Publish.md
```

## Step 7: Verify TitleCase

Run this check:
```bash
ls ${SKILLS_HOME}/[SkillName]/
ls ${SKILLS_HOME}/[SkillName]/Workflows/
ls ${SKILLS_HOME}/[SkillName]/Tools/
```

Verify ALL files use TitleCase:
- `SKILL.md` ✓ (exception - always uppercase)
- `WorkflowName.md` ✓
- `ToolName.ts` ✓
- `ToolName.help.md` ✓

## Step 8: Create RATIONALE.md

Every custom skill gets a RATIONALE.md alongside its SKILL.md. This documents WHY it was built, not just what it does.

```bash
touch ${SKILLS_HOME}/[SkillName]/RATIONALE.md
```

Write the following template, filling in what you know:

```markdown
# [SkillName] — Design Document

**Created:** [today's date]
**Origin:** [which project/session it was built in, or "external" if adopted]
**Status:** Active
**Last verified:** [today's date — update when you confirm the doc matches the code]

## Why This Exists

[2-3 sentences: what problem does this solve? Why was a skill needed instead of a one-off solution?]

## Architecture

[How it works — sub-skills, workflow routing, key patterns, external dependencies]

## Key Design Decisions

- [Non-obvious choice and why]
- [Alternative considered and why rejected]

## Custom Workflows

| Workflow | Description | Custom? |
|----------|-------------|---------|
| [WorkflowOne] | [What it does] | Yes — built for [reason] |

## Known Issues

- [Any bugs, limitations, dead code, or rough edges]

## Related

- [Links to other skills, design specs, or project memories this connects to]
```

**For simple skills (1-2 workflows):** Fill in Why + Architecture + one design decision. Keep it brief.
**For complex skills (3+ workflows):** Fill in all sections thoroughly. This is the deep-dive that future sessions will read.

The `GenerateCapabilityCatalog.ts` tool will warn if a skill is missing RATIONALE.md, so this doesn't get forgotten.

## Step 9: Final Checklist

### Naming (TitleCase)
- [ ] Skill directory uses TitleCase (e.g., `Blogging`, `Daemon`)
- [ ] All workflow files use TitleCase (e.g., `Create.md`, `UpdateInfo.md`)
- [ ] All reference docs use TitleCase (e.g., `ProsodyGuide.md`)
- [ ] All tool files use TitleCase (e.g., `ManageServer.ts`)
- [ ] Routing table workflow names match file names exactly

### YAML Frontmatter
- [ ] `name:` uses TitleCase
- [ ] `description:` is single-line with embedded `USE WHEN` clause
- [ ] No separate `triggers:` or `workflows:` arrays
- [ ] Description uses intent-based language
- [ ] Description is under 1024 characters

### Markdown Body
- [ ] `## Voice Notification` section present (for skills with workflows)
- [ ] `## Workflow Routing` section with table format
- [ ] All workflow files have routing entries
- [ ] `## Examples` section with 2-3 concrete usage patterns

### Structure
- [ ] `tools/` directory exists (even if empty)
- [ ] No `backups/` directory inside skill

### Documentation
- [ ] `RATIONALE.md` exists alongside SKILL.md
- [ ] RATIONALE.md has at least: Why This Exists, Architecture, Key Design Decisions
- [ ] Complex skills (3+ workflows): all RATIONALE.md sections filled in

### CLI-First Integration (for skills with CLI tools)
- [ ] CLI tools expose configuration via flags (see CliFirstArchitecture.md)
- [ ] Workflows that call CLI tools have intent-to-flag mapping tables
- [ ] Flag mappings cover: mode selection, output options, post-processing (where applicable)

## Done

Skill created following canonical structure with proper TitleCase naming and RATIONALE.md documentation.
