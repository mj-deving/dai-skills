---
name: ScientificDeck
description: Scientific presentation generation — LaTeX Beamer decks and self-contained HTML slide decks using Scott Cunningham's Rhetoric of Decks framework. USE WHEN scientific presentation, beamer deck, academic slides, scientific slides, compile deck, latex presentation, html deck, scientific html slides, academic presentation, rhetoric of decks, compile tex, new research project.
---

# ScientificDeck

Scientific presentations in two formats: LaTeX Beamer (journal-ready PDFs) and self-contained HTML (interactive, zero-setup). Both apply Scott Cunningham's Rhetoric of Decks: Beauty=Clarity, one-idea-per-slide, assertive titles.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/ScientificDeck/`

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CompileDeck** | "compile deck", "create presentation", "beamer deck", "scientific slides" | `Workflows/CompileDeck.md` |
| **CompileTex** | "compile tex", "fix latex", "latex errors" | `Workflows/CompileTex.md` |
| **NewProject** | "new research project", "scaffold project" | `Workflows/NewProject.md` |
| **GenerateHtmlDeck** | "html deck", "scientific html slides", "academic presentation html" | `Workflows/GenerateHtmlDeck.md` |

## Examples

**Example 1: Create a LaTeX Beamer presentation**
```
User: "Create a scientific presentation on causal inference methods"
→ Invokes CompileDeck workflow
→ Generates LaTeX Beamer slides with Rhetoric of Decks principles
→ Compiles to PDF
```

**Example 2: Create an interactive HTML deck**
```
User: "Make scientific html slides about regression discontinuity"
→ Invokes GenerateHtmlDeck workflow
→ Generates self-contained HTML with KaTeX equations, Chart.js figures
→ Opens in any browser, no setup required
```

**Example 3: Fix LaTeX compilation errors**
```
User: "Fix the latex errors in my presentation"
→ Invokes CompileTex workflow
→ Reads error log, fixes specific issues
→ Recompiles to zero-warning standard
```

## Format Comparison

| Factor | LaTeX (CompileDeck) | HTML (GenerateHtmlDeck) |
|--------|-------------------|----------------------|
| Setup | texlive required | Zero — browser only |
| Output | PDF | Self-contained HTML |
| Equations | Native LaTeX (perfect) | KaTeX (good) |
| Interactivity | Static | Charts, hover, animations |
| Journal-ready | Yes | No |

## Context Files (load on demand)

**LaTeX:** `RhetoricOfDecks.md`, `BeamerPatterns.md`, `MultiAgentReview.md`, `QualityChecklist.md`
**HTML:** `HtmlRhetoricAdapted.md`, `HtmlSlideEngine.md`, `HtmlAcademicPatterns.md`, `HtmlQualityChecklist.md`

## Source

Adapted from Scott Cunningham's Rhetoric of Decks framework. Reference: `~/projects/Pai-Exploration/References/Rhetoric-of-Decks/`
