---
name: Typst
description: "Professional PDF document creation via Typst — CVs, cover letters, reports, proposals, invoices, technical docs, academic papers, flyers, posters, brochures. USE WHEN create PDF, generate PDF, make PDF, CV, resume, cover letter, application letter, report PDF, proposal, invoice, technical document, academic paper, typst, format as PDF, export PDF, professional document, letter, letterhead, flyer, poster, brochure, handout, leaflet, marketing print, print design."
---

# Typst — Professional PDF Creation

Create publication-quality PDFs using Typst, a modern markup-based typesetting system.

**CLI:** `typst compile input.typ output.pdf` (sub-second compilation, single binary, no dependencies)

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| CV, resume, curriculum vitae | `Workflows/CV.md` |
| Cover letter, application letter, motivation letter | `Workflows/Letter.md` |
| Report, research report, findings, analysis report | `Workflows/Report.md` |
| Proposal, SOW, consulting document, business proposal | `Workflows/Proposal.md` |
| Invoice, receipt, billing document | `Workflows/Invoice.md` |
| Technical doc, architecture spec, API doc, runbook | `Workflows/TechnicalDoc.md` |
| Academic paper, thesis, scientific paper, research paper | `Workflows/AcademicPaper.md` |
| Flyer, poster, brochure, handout, leaflet, marketing print | `Workflows/Flyer.md` |
| Any other PDF, generic document | `Workflows/Generic.md` |

## How It Works

1. Claude generates a `.typ` file (Typst markup)
2. `typst compile doc.typ doc.pdf` produces the PDF
3. Open in browser or PDF viewer to verify

## Typst Quick Reference

```typst
// Headings
= Title
== Section
=== Subsection

// Emphasis
*bold* _italic_ `code`

// Lists
- Bullet item
+ Numbered item

// Links
#link("https://example.com")[Display text]

// Images
#image("photo.jpg", width: 50%)

// Tables
#table(
  columns: (1fr, 2fr),
  [*Header 1*], [*Header 2*],
  [Cell 1], [Cell 2],
)

// Page setup
#set page(paper: "a4", margin: 2cm)
#set text(font: "Libertinus Serif", size: 11pt)

// Functions
#let accent = rgb("#2563eb")
```

## PAI House Style

Default styling for PAI-generated documents:

```typst
// PAI defaults — clean, professional, European
#set page(paper: "a4", margin: (top: 2.5cm, bottom: 2cm, left: 2.5cm, right: 2.5cm))
#set text(font: "Libertinus Serif", size: 11pt, lang: "en")
#set heading(numbering: "1.1")
#set par(justify: true, leading: 0.65em)

#let pai-accent = rgb("#1e3a5f")  // Deep navy
#let pai-light = rgb("#f0f4f8")   // Soft background
```

Workflows override these defaults per document type (e.g., CV uses sans-serif, letters use larger margins).

### Available Fonts (verified installed)

| Purpose | Font | Fallback |
|---------|------|----------|
| Body serif | Libertinus Serif | Liberation Serif |
| Body sans | Ubuntu Sans | Liberation Sans |
| Headings sans | Ubuntu Sans | Liberation Sans |
| Monospace | Ubuntu Mono | DejaVu Sans Mono |
| Display | Latin Modern Roman | Libertinus Serif |

**Always use fonts from this list.** Run `typst fonts` to verify if others are needed.

## Community Templates

Typst Universe has 1200+ packages. Use `typst init @preview/package-name` to scaffold from a community template.

**Curated picks:**
- CV: `@preview/modern-cv`, `@preview/basic-resume`, `@preview/brilliant-cv`
- Letters: `@preview/letter-pro`, `@preview/appreciated-letter`
- Reports: `@preview/charged-ieee`, `@preview/clean-report`
- Academic: `@preview/ilm`, `@preview/scholarly`

To use: `typst init @preview/modern-cv my-cv` then edit the generated files.

## Integration with Other PAI Skills

| Source Skill | How to Pipe | Output |
|-------------|-------------|--------|
| Research | "generate PDF report from research" | Formatted findings report |
| ScientificDeck | "export deck as PDF" | Slide handout PDF |
| VisualExplainer | "export as PDF" | Diagram/table PDF |
| ContentAnalysis | "format analysis as PDF" | Structured analysis report |
| Telos | "export goals/projects as PDF" | Life dashboard PDF |

## File Organization

Generated documents go in the current working directory:
- `{name}.typ` — Typst source (editable)
- `{name}.pdf` — Compiled output
