# Skillgrade Workflow

External skill-level eval runner. Docker-sandboxed, multi-agent, deterministic + LLM rubric graders.

**Repo:** https://github.com/mgechev/skillgrade (Minko Gechev, Angular team at Google)
**Installed:** v0.1.3 via npx

## What It Does

Tests skills from the OUTSIDE — gives an agent a task in a Docker container, checks if it produces the right output. Complements PAI's internal Evals (which test Algorithm behavior from the INSIDE).

| skillgrade | PAI Evals |
|------------|-----------|
| Tests: does the skill produce correct output? | Tests: did the Algorithm follow its rules? |
| Docker-sandboxed, clean slate per trial | Runs in local environment |
| Multi-agent (Gemini, Claude, Codex) | Claude-only via `claude -p` |
| `eval.yaml` single-file config | Multi-file YAML tasks + suite management |
| Good for: isolated skill testing | Good for: system-level behavioral testing |

## CLI Quick Reference

```bash
# Generate eval.yaml by reading the SKILL.md in cwd
cd ${SKILLS_HOME}/{SkillName}
npx skillgrade init

# Run all evals (requires Docker + agent API key)
npx skillgrade

# Presets
npx skillgrade --smoke           # 5 trials, reports pass@k
npx skillgrade --reliable        # 15 trials, reports mean reward
npx skillgrade --regression      # 30 trials, reports pass^k

# Run specific eval
npx skillgrade --eval=trivy-vulnerability-scan

# Run only deterministic graders (no LLM cost)
npx skillgrade --grader=deterministic

# Override agent
npx skillgrade --agent=claude
npx skillgrade --agent=gemini
npx skillgrade --agent=codex

# CI mode — exit non-zero if below threshold
npx skillgrade --regression --ci --threshold=0.8

# Validate graders against reference solutions before running
npx skillgrade --validate

# View results
npx skillgrade preview           # CLI table
npx skillgrade preview browser   # Web UI at localhost:3847
```

## eval.yaml Format

```yaml
version: "1"

defaults:
  agent: gemini
  provider: docker
  trials: 3
  timeout: 300
  threshold: 0.8
  docker:
    base: node:20-slim

tasks:
  - name: task-name
    instruction: |
      What to tell the agent to do.
    workspace:                          # Optional fixture files
      - src: |
          file contents here
        dest: filename.json
    graders:
      - type: deterministic             # Bash script, 70% weight typical
        run: |
          # Check outputs, echo JSON: {"score":0.67,"details":"2/3 passed","checks":[...]}
        weight: 0.7
      - type: llm_rubric                # LLM judges quality, 30% weight typical
        rubric: |
          What the agent should have done correctly.
        weight: 0.3
```

## Initialized Skills

These skills have `eval.yaml` files ready to run:

| Skill | Tasks | What They Test |
|-------|-------|----------------|
| Security | `trivy-vulnerability-scan`, `sops-secrets-encryption` | Trivy scan finds CRITICALs; sops encrypts secrets with age key |
| VisualExplainer | `generate-architecture-diagram`, `generate-slide-deck` | Produces self-contained HTML with Mermaid diagrams; slide structure |
| GSD | `gsd-initialize-project`, `gsd-map-codebase` | Creates .planning dir + roadmap; analyzes existing codebase |

## When to Use

- **New skill adoption** — run `skillgrade init` to auto-generate baseline evals
- **Skill regression testing** — after modifying a skill, verify it still works
- **Multi-agent comparison** — same eval against Gemini vs Claude vs Codex
- **CI gates** — `--ci --threshold=0.8` for automated quality checks

## Adding Evals to More Skills

```bash
cd ${SKILLS_HOME}/{SkillName}
npx skillgrade init          # Gemini reads SKILL.md, generates eval.yaml
# Review and edit eval.yaml — init output is a starting point, not final
npx skillgrade --validate    # Verify graders work with reference solutions
npx skillgrade --smoke       # Quick 5-trial test
```

`skillgrade init` uses Gemini to read the SKILL.md and auto-generate tasks + graders. Always review the output — it's a scaffold, not production-ready.
