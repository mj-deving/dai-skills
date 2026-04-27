---
name: VisualExplainer
description: Generate self-contained HTML pages for diagrams, diff reviews, slide decks, data tables, and visual plans. USE WHEN generate diagram, visual explanation, diff review, code review visualization, generate slides, slide deck, visual plan, project recap visualization, fact check report, web diagram, architecture diagram, flowchart HTML, data table visualization, visual documentation, render as HTML instead of ASCII, or share diagram. Replaces ASCII tables and text diagrams with interactive browser-rendered HTML.
---

# VisualExplainer

Turns complex terminal output into styled, interactive HTML pages. Visual is default — prose is accent. For Mermaid diagrams: use this skill for interactive HTML with zoom/pan; use Media/Art for static image exports (PNG/SVG for slides or docs).

## Quality References (load on demand)

Before generating HTML output, consult these checklists:
- **Performance:** `${SKILLS_HOME}/Utilities/References/performance-checklist.md` — Core Web Vitals, bundle budgets, image optimization, rendering best practices
- **Accessibility:** `${SKILLS_HOME}/Utilities/References/accessibility-checklist.md` — WCAG 2.1 AA, keyboard nav, screen reader support, color contrast, ARIA patterns

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table (4+ rows or 3+ columns), generate an HTML page instead. Don't wait for the user to ask — render it as HTML automatically and tell them the file path.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/VisualExplainer/`

If this directory exists, load and apply any PREFERENCES.md. If not, proceed with defaults.

<!-- ## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the VisualExplainer skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **VisualExplainer** skill to ACTION...
   ```
-->

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **GenerateWebDiagram** | "diagram", "flowchart", "visualize architecture" | `Workflows/GenerateWebDiagram.md` |
| **GenerateVisualPlan** | "visual plan", "implementation plan", "feature spec" | `Workflows/GenerateVisualPlan.md` |
| **GenerateSlides** | "slides", "slide deck", "presentation" | `Workflows/GenerateSlides.md` |
| **DiffReview** | "diff review", "review this diff", "visual code review" | `Workflows/DiffReview.md` |
| **PlanReview** | "review plan", "plan assessment", "plan coverage" | `Workflows/PlanReview.md` |
| **ProjectRecap** | "project recap", "recap", "re-entry context" | `Workflows/ProjectRecap.md` |
| **FactCheck** | "fact check", "verify claims", "check document" | `Workflows/FactCheck.md` |
| **ShareDiagram** | "share diagram", "deploy diagram", "publish HTML" | `Workflows/ShareDiagram.md` |
| **InteractiveBrainstorm** | "brainstorm visually", "show design options", "interactive mockup", "visual companion" | `BrainstormServer/` (see below) |

## Examples

**Example 1: Architecture diagram**
```
User: "Generate a diagram of the authentication flow"
→ Invokes GenerateWebDiagram workflow
→ Reads CssPatterns.md + Libraries.md for rendering approach
→ Generates Mermaid flowchart with zoom/pan controls
→ Opens ${AGENT_HOME}/diagrams/auth-flow.html in browser
```

**Example 2: Diff review**
```
User: "Give me a visual diff review of the last commit"
→ Invokes DiffReview workflow
→ Gathers git diff, file stats, API surface changes
→ Generates 9-section HTML report with KPI dashboard
→ Opens in browser with architecture diagrams and code analysis
```

**Example 3: Slide deck**
```
User: "Turn this research into slides"
→ Invokes GenerateSlides workflow
→ Plans narrative arc, selects slide types
→ Generates deck with keyboard/touch navigation
→ Opens presentation in browser
```

## InteractiveBrainstorm Workflow

Live visual brainstorming via a zero-dependency Node.js server. Claude writes HTML fragments with `data-choice` attributes, the user sees them in a browser and clicks choices, Claude reads those choices on the next turn.

**Steps:**
1. Start server: `bash BrainstormServer/start-server.sh --project-dir $(pwd)`
2. Write HTML fragments with `data-choice` attributes to the session directory (from the JSON output)
3. Share the URL with the user (e.g. `http://127.0.0.1:3333`)
4. Read choices from `.events` file in the session directory on next turn
5. Stop server when done: `bash BrainstormServer/stop-server.sh <session-dir>`

**Example fragment:**
```html
<h2>Which layout do you prefer?</h2>
<div class="choice-grid">
  <div data-choice="sidebar">Sidebar navigation with collapsible sections</div>
  <div data-choice="topnav">Top navigation bar with dropdown menus</div>
  <div data-choice="tabs">Tabbed interface with persistent state</div>
</div>
```

See `BrainstormServer/RATIONALE.md` for architecture details.

## Quick Reference

**Output:** `${AGENT_HOME}/diagrams/{descriptive-name}.html` (opens in browser)
**Renderers:** Mermaid.js (diagrams), CSS Grid (cards), Chart.js (metrics), HTML table (data)
**Themes:** Light + dark via CSS custom properties
**Anti-slop:** No Inter/violet, no neon dashboards, no gradient mesh

**Context files (load on demand):**
- `CssPatterns.md` — Layout, theming, animations, overflow protection
- `Libraries.md` — CDN links, Mermaid theming, 13 font pairings
- `SlidePatterns.md` — Slide engine, 10 types, presets
- `ResponsiveNav.md` — Sticky TOC, scroll-spy
- `AntiPatterns.md` — AI slop detection, forbidden patterns
- `QualityChecklist.md` — Squint/swap/theme/overflow/zoom checks
- `MasterReference.md` — Full SKILL.md from original visual-explainer (workflow, diagram types, aesthetics)
