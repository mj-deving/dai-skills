# IdeaGeneration Workflow

<!-- ## Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the IdeaGeneration workflow in the BeCreative skill to brainstorm solutions"}' \
  > /dev/null 2>&1 &
```

Running **IdeaGeneration** in **BeCreative**...

---

**When to use:** Brainstorming, problem-solving, innovation, refining raw ideas into actionable concepts

---
-->

## Process

### Phase 1: Reframe — "How Might We"

Before generating solutions, reframe the problem as an opportunity:

- Restate the user's problem as a "How Might We ___?" question
- This shifts from problem-focus to solution-focus
- Example: "Auth is too complex" → "How might we make auth invisible to the user?"

### Phase 2: Generate — Named Exploration Lenses

In your thinking, generate 5+ diverse approaches using Verbalized Sampling (p<0.10 each). Apply these named lenses to ensure structural diversity:

| Lens | Question |
|------|----------|
| **Inversion** | What if we did the exact opposite? |
| **Constraint Removal** | What if budget/time/tech were unlimited? |
| **Simplification** | What's the 1-feature version? |
| **Combination** | What if we merged two unrelated approaches? |
| **Scale Shift** | What if this was for 10x or 0.1x the audience? |
| **Analogy** | How does a completely different industry solve this? |

Not every lens applies to every problem — use the ones that produce genuine diversity.

### Phase 3: Evaluate — Cluster and Stress-Test

1. **Cluster** resonant ideas — which variations point in the same direction?
2. **Stress-test** the top 2-3 clusters against:
   - User value — does this solve the actual problem?
   - Feasibility — can this be built with available resources?
   - Differentiation — is this genuinely different from obvious solutions?
3. **Surface hidden assumptions** — what are you taking for granted?

### Phase 4: Sharpen — Structured One-Pager Output

Present the recommended direction as a structured one-pager:

```markdown
## [Idea Title]

**Problem:** [The HMW question]
**Direction:** [Recommended approach in 2-3 sentences]
**Key Assumptions:** [What must be true for this to work]
**MVP Scope:** [Smallest version that validates the direction]
**Not Doing:** [Explicit scope boundaries — what this deliberately excludes]
```

The "Not Doing" list is arguably the most valuable part — it prevents scope creep by making exclusions explicit upfront.

---

## Best For

- Strategic planning and product direction
- Business innovation and new opportunities
- Technical problem-solving and architecture decisions
- Product development and feature scoping
- Process improvement and workflow design

---

## Key Principles

- **Simplicity is the ultimate sophistication** — prefer the simplest version that works
- **Prioritize UX before technology** — what does the user need, not what's technically interesting
- **Challenge assumptions** — the best ideas come from questioning what everyone takes for granted
- **Say no to breadth** — focus beats feature lists
