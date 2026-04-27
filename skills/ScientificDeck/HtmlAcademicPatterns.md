# Academic HTML Patterns

## Equations (KaTeX)
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body)"></script>
```
Display: `$$Y_i = \alpha + \beta T_i + \varepsilon_i$$`
Inline: `$\beta$ represents the treatment effect`

## Charts (Chart.js)
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
```

## Diagrams (Mermaid)
```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'base' });
</script>
```

## Academic Tables
```css
.academic-table { width: 100%; border-collapse: collapse; }
.academic-table thead { border-bottom: 2px solid var(--text); }
.academic-table td { padding: 6px 16px; border-bottom: 1px solid var(--border); }
.academic-table .sig { color: var(--accent); }
.academic-table .se { color: var(--text-dim); font-size: 0.85em; }
```

## Slide Types
- **Title**: Large display + author + institution
- **Section Divider**: Large number + section title
- **Content**: Heading + bullets/prose
- **Data**: Heading + table or chart
- **Figure**: Full-bleed image + caption
- **Two-Column**: Content left + figure right
- **Quote**: Large serif italic + attribution
- **Results**: Regression table with significance stars
