# Proposal / Business Document Workflow

Generate professional proposals, SOWs, consulting reports, or pitch documents as PDF.

## Community Templates

Use community templates first — don't reinvent the wheel:

```bash
# Business report with cover page, TOC, infoboxes, tables, author cutout
typst init @preview/biz-report proposal
# Clean general-purpose document
typst init @preview/guido proposal     # (needs Nunito font installed)
# Simple colorful template
typst init @preview/bubble proposal
```

**Recommended:** `@preview/biz-report` — has cover page, TOC, infoboxes, tables, document control section, and back page. Production-quality out of the box.

## Structure

```
Cover page (title, client name, date, your logo)
Table of contents
Executive summary
Problem statement / Opportunity
Proposed solution
Scope of work / Deliverables
Timeline / Milestones
Pricing / Investment
Terms and conditions
About us / Team
```

## PAI Fallback Template

If community templates don't fit, use PAI house style:

```typst
#set page(paper: "a4", margin: 2.5cm)
#set text(font: "Libertinus Serif", size: 11pt)
#set heading(numbering: "1.1")
#set par(justify: true)
#show outline.entry.where(level: 1): it => strong(it)

#let accent = rgb("#1e3a5f")

// Cover page
#page(margin: 0)[
  #rect(fill: accent, width: 100%, height: 40%)[
    #align(center + horizon)[
      #text(white, size: 28pt, weight: "bold")[Proposal Title]
      #v(0.5em)
      #text(white, size: 14pt)[Prepared for Client Name]
      #v(0.3em)
      #text(white.darken(20%), size: 11pt)[#datetime.today().display("[month repr:long] [year]")]
    ]
  ]
]

#outline(indent: auto)
#pagebreak()

= Executive Summary
// ...
```

## Compile
```bash
typst compile proposal/main.typ proposal.pdf
```
