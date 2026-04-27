# Academic Paper Workflow

Generate academic papers, conference submissions, or research papers as PDF.

## Community Templates

The academic category is Typst's strongest — 87+ packages for specific journals and conferences.

```bash
# IEEE format (most common engineering/CS conferences)
typst init @preview/charged-ieee paper

# Clean math paper
typst init @preview/clean-math-paper paper

# Generic academic with homework/problem sets
typst init @preview/academic-alt paper

# Problem sets for technical courses
typst init @preview/adaptable-pset pset

# Academic conference presentation
typst init @preview/academic-conf-pre slides

# Homework + slides combined
typst init @preview/axiomst assignment
```

**Recommended:** `@preview/charged-ieee` for CS/engineering papers. `@preview/clean-math-paper` for math-heavy work.

## Specific Journal/Conference Templates

Many conferences have dedicated Typst templates:
- IEEE: `@preview/charged-ieee`
- ACM: search `acm` on Typst Universe
- IFAC: `@preview/abiding-ifacconf`
- JACoW (accelerator physics): `@preview/accelerated-jacow`
- LNCS (Springer): search `lncs` on Typst Universe

Check `typst init --list` or https://packages.typst.org for your specific venue.

## Math Support

Typst has native math — no packages needed:

```typst
// Inline math
The loss function $L(theta) = -sum_(i=1)^N log p(y_i | x_i, theta)$

// Display math
$ integral_0^infinity e^(-x^2) dif x = sqrt(pi) / 2 $

// Aligned equations
$ f(x) &= x^2 + 2x + 1 \
       &= (x + 1)^2 $
```

## PAI Academic Template

```typst
#set page(paper: "a4", margin: (top: 2.5cm, bottom: 2.5cm, left: 2cm, right: 2cm))
#set text(font: "Libertinus Serif", size: 11pt)
#set heading(numbering: "1.1")
#set par(justify: true, first-line-indent: 1em)
#set math.equation(numbering: "(1)")
#set figure(gap: 0.8em)

// Title block
#align(center)[
  #text(size: 16pt, weight: "bold")[Paper Title: Descriptive and Specific]
  #v(0.8em)
  #text(size: 11pt)[Author Name#super[1], Co-Author Name#super[2]]
  #v(0.3em)
  #text(size: 9pt, style: "italic")[
    #super[1]Institution One, City, Country \
    #super[2]Institution Two, City, Country
  ]
  #v(0.5em)
  #text(size: 9pt)[Corresponding author: author\@institution.edu]
]

#v(1em)

// Abstract
#block(inset: (left: 2em, right: 2em))[
  *Abstract* — Brief summary of the paper's contribution, methods, and key findings. Keep under 200 words for most venues.
]

#v(0.5em)
#text(size: 9pt)[*Keywords:* keyword1, keyword2, keyword3]

#v(1em)

= Introduction
// ...

= Related Work
// ...

= Method
// ...

= Results
// ...

= Conclusion
// ...

// Bibliography
#bibliography("refs.bib")
```

## Bibliography

Typst supports `.bib` files natively:

```typst
// In the paper
@smith2024 showed that...
As demonstrated in previous work @jones2023.

// At the end
#bibliography("refs.bib", style: "ieee")
```

## Compile
```bash
typst compile paper/main.typ paper.pdf
```
