# CompileDeck Workflow

Generate a scientific Beamer presentation from content.

## Trigger
"compile deck", "create presentation", "beamer deck", "scientific slides"

## Steps

### Step 1: Audience & Style
Ask two questions:
1. **Audience:** External (seminars/conferences) or Internal (coauthors)?
2. **Style:** Professional house style or unique creative design?

### Step 2: Content Planning
- Determine narrative arc based on content type
- Map content to slides (one idea per slide)
- Plan figures (which need R/Python generation?)
- Estimate slide count (~1 per minute of talk)

### Step 3: Code-First Figures
For each planned figure:
1. Write R or Python script in `code/figures/`
2. Execute script to generate PDF/PNG in `output/figures/`
3. Verify figure renders correctly

### Step 4: Generate LaTeX
- Load `RhetoricOfDecks.md` principles
- Load `BeamerPatterns.md` templates
- Generate .tex file with assertive titles
- Use `\includegraphics` for pre-generated figures

### Step 5: Compile & Fix
```bash
pdflatex -interaction=nonstopmode main.tex
```
Fix ALL warnings. Iterate until zero-warning compile.

### Step 6: Multi-Agent Review
Invoke review cycle from `MultiAgentReview.md`:
1. Reviewer checks narrative flow
2. Graphics Specialist checks visual correctness
3. Apply fixes, recompile

### Step 7: Deliver
- Verify against `QualityChecklist.md`
- Output: `presentations/main.pdf`
