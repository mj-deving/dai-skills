# GenerateScientificDeck Workflow

## Trigger
"scientific html slides", "html deck", "academic presentation html"

## Steps

### Step 1: Input & Audience
- Topic or source document
- Audience: External / Internal / Students
- Talk duration → slide count
- Needs: equations? charts? diagrams?

### Step 2: Planning
Load `RhetoricAdapted.md`. Determine arc, map slides, choose types, select typography + palette.

### Step 3: Generation
Load `SlideEngine.md` + `AcademicPatterns.md`. Generate self-contained HTML (all CSS/JS inline, CDNs for KaTeX/Chart.js/Mermaid).

### Step 4: Review
Apply `QualityChecklist.md` — content, technical, visual, navigation passes.

### Step 5: Output
Save to `~/.agent/diagrams/` or project presentations/ directory. Open in browser.
