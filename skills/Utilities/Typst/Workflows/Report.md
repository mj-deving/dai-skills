# Report Workflow

Generate a professional report PDF — research findings, analysis, recommendations.

## When to Use
- Research skill output → formatted PDF report
- Business analysis, market research, technical findings
- Any structured "here's what we found" document

## Template Structure

```
Cover page (title, author, date, optional logo)
Table of contents (auto-generated)
Executive summary (1 page max)
Sections with findings
Conclusions / recommendations
Appendix (optional)
```

## PAI Report Defaults

```typst
#set page(paper: "a4", margin: 2.5cm, header: context {
  if counter(page).get().first() > 1 [
    #text(size: 9pt, fill: rgb("#6b7280"))[Report Title — #datetime.today().display()]
    #line(length: 100%, stroke: 0.3pt + rgb("#d1d5db"))
  ]
})
#set text(font: "Libertinus Serif", size: 11pt)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(1cm)
  text(rgb("#1e3a5f"), size: 18pt, weight: "bold", it)
  v(0.5cm)
}
```

## Compile
```bash
typst compile report.typ report.pdf
```
