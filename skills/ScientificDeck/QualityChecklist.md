# Quality Checklist — Zero-Warning Standard

## Compilation Standard

**Zero tolerance:** Every compile must be completely clean — no overfull hbox (not even 0.5pt), no underfull vbox, no font warnings. All LaTeX warnings are treated as errors.

## Compilation Verification

```bash
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "Warning|Error|Overfull|Underfull"
# Expected output: empty (no matches)
```

## Silent Error Categories

These errors compile without warnings but look wrong:

| Category | Example | Detection |
|----------|---------|-----------|
| **TikZ misalignment** | Labels shifted from intended position | Visual inspection of coordinates |
| **Text overlap** | ggplot labels running into each other | Check at actual slide dimensions |
| **Clipped figures** | Image extends beyond frame boundary | Check \includegraphics scaling |
| **Font substitution** | Intended font silently replaced | Check log for "Font shape not found" |
| **Color issues** | Indistinguishable colors for colorblind | Check with colorblind simulator |
| **Table overflow** | Column too wide for frame | Check at 169 aspect ratio |

## Pre-Delivery Checklist

- [ ] `pdflatex` produces zero warnings
- [ ] All figures render at correct size
- [ ] All titles are assertive claims
- [ ] One idea per slide
- [ ] Narrative arc is coherent
- [ ] Audience calibration matches target
- [ ] Figures generated from code (reproducible)
- [ ] No hardcoded file paths
- [ ] Bibliography compiles (if used)
- [ ] Slide count matches talk duration (~1 slide/minute)
