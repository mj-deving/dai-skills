# Generic Document Workflow

Catch-all for any PDF that doesn't fit CV, Letter, Report, Proposal, Invoice, Technical, or Academic patterns.

## Approach

1. Ask the user what kind of document they need
2. Apply PAI house style defaults
3. Generate Typst source with appropriate structure
4. Compile and verify

## PAI Generic Defaults

```typst
#set page(paper: "a4", margin: 2.5cm)
#set text(font: "Libertinus Serif", size: 11pt)
#set heading(numbering: "1.1")
#set par(justify: true, leading: 0.65em)

#let accent = rgb("#1e3a5f")
```

## If the user wants a community template

```bash
# Browse available templates
typst init --list

# Scaffold from a specific template
typst init @preview/template-name my-document
cd my-document
# Edit the generated .typ file
typst compile main.typ
```

## Compile
```bash
typst compile document.typ document.pdf
```
