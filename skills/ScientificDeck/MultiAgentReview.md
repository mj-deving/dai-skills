# Multi-Agent Review Cycle

Three-agent sequential review ensuring presentation quality. Each agent catches distinct error categories.

## Agent 1: Builder

**Role:** Creates initial LaTeX structure.
**Workflow:**
1. Generate Beamer LaTeX based on content outline
2. Run R/Python code first to generate all figures
3. Insert figures into LaTeX
4. Compile initial version
5. Fix all compilation errors

**Output:** Compilable .tex file + generated figures

## Agent 2: Reviewer

**Role:** Checks narrative flow and information density.
**Checklist:**
- [ ] Every slide has exactly one idea
- [ ] All titles are assertive claims (not labels)
- [ ] Narrative follows chosen arc (Problem→Investigation→Resolution)
- [ ] Cognitive load distributed evenly (no dense-then-sparse)
- [ ] MB > MC for every element on every slide
- [ ] Audience calibration correct (external/internal/student)
- [ ] No orphan slides (every slide connects to the arc)

**Output:** Review report with specific slide-level feedback

## Agent 3: Graphics Specialist

**Role:** Catches silent visual errors that compile without warnings.
**Checklist:**
- [ ] TikZ coordinates are correct (labels don't overlap)
- [ ] ggplot/matplotlib text is readable at presentation size
- [ ] Figure scaling is appropriate (\textwidth vs custom)
- [ ] Table alignment is correct (decimal points, column widths)
- [ ] Colors are distinguishable (colorblind-safe)
- [ ] No clipped content (figures/tables fit within frame)

**Output:** Graphics report with specific fixes

## Invocation

```
Phase 1: Builder agent creates deck
Phase 2: Reviewer agent audits narrative
Phase 3: Graphics agent audits visuals
Phase 4: Builder applies fixes from both reviews
Phase 5: Final compilation → zero warnings
```
