# Technical Document Workflow

Generate technical documentation — architecture specs, API docs, runbooks, READMEs as PDF.

## Community Templates

```bash
# Clean general-purpose document with good code block styling
typst init @preview/bubble techdoc

# Simple report with clean structure
typst init @preview/basic-report techdoc
```

## Structure

Technical docs vary widely. Common patterns:

**Architecture Spec:**
```
Title + version + date
Overview / Context
System architecture diagram (describe, or include image)
Component descriptions
Data flow
API contracts
Non-functional requirements
Deployment architecture
Decision log
```

**Runbook:**
```
Service name + owner
Prerequisites
Common procedures (deploy, rollback, restart)
Troubleshooting decision tree
Escalation contacts
```

## PAI Technical Doc Template

```typst
#set page(paper: "a4", margin: 2cm, header: context {
  if counter(page).get().first() > 1 [
    #text(size: 8pt, fill: rgb("#9ca3af"))[TECHNICAL DOCUMENT — v1.0]
    #h(1fr)
    #text(size: 8pt, fill: rgb("#9ca3af"))[CONFIDENTIAL]
    #line(length: 100%, stroke: 0.3pt + rgb("#e5e7eb"))
  ]
})
#set text(font: "Ubuntu Sans", size: 10pt)
#set heading(numbering: "1.1")
#set par(justify: true)
#show raw.where(block: true): it => block(
  fill: rgb("#f8fafc"),
  stroke: 0.5pt + rgb("#e2e8f0"),
  inset: 10pt,
  radius: 4pt,
  width: 100%,
  it,
)

#let accent = rgb("#1e3a5f")
#let note(body) = block(
  fill: rgb("#eff6ff"),
  stroke: 0.5pt + rgb("#93c5fd"),
  inset: 10pt,
  radius: 4pt,
  width: 100%,
)[#text(rgb("#1e40af"), weight: "bold", size: 9pt)[NOTE:] #body]

#let warning(body) = block(
  fill: rgb("#fef3c7"),
  stroke: 0.5pt + rgb("#f59e0b"),
  inset: 10pt,
  radius: 4pt,
  width: 100%,
)[#text(rgb("#92400e"), weight: "bold", size: 9pt)[WARNING:] #body]

// Title
#align(center)[
  #text(accent, size: 22pt, weight: "bold")[Document Title]
  #v(0.3em)
  #text(size: 11pt)[Version 1.0 — #datetime.today().display("[month repr:long] [day], [year]")]
  #v(0.2em)
  #text(rgb("#6b7280"), size: 10pt)[Author Name]
]

#v(1em)
#outline(indent: auto)
#pagebreak()

= Overview
// Content...

= Architecture
// Content + diagrams...

== Components
// ...
```

## Code Blocks

Typst has built-in syntax highlighting:

````typst
```python
def hello():
    print("Hello from Typst")
```
````

## Compile
```bash
typst compile techdoc.typ techdoc.pdf
```
