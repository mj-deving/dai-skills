# Quality Checks

Before delivering any generated HTML page, verify all of these:

1. **The squint test** — Blur your eyes. Can you still perceive hierarchy? Are sections visually distinct?
2. **The swap test** — Would replacing your fonts and colors with a generic dark theme make this indistinguishable from a template? If yes, push the aesthetic further.
3. **Both themes** — Toggle between light and dark mode. Both should look intentional, not broken.
4. **Information completeness** — Does the diagram convey what the user asked for? Pretty but incomplete is a failure.
5. **No overflow** — Resize browser to different widths. No content should clip or escape its container. Every grid/flex child needs `min-width: 0`. Side-by-side panels need `overflow-wrap: break-word`. Never `display: flex` on `<li>` for markers.
6. **Mermaid zoom controls** — Every `.mermaid-wrap` must have zoom controls (+/-/reset/expand), Ctrl/Cmd+scroll zoom, click-and-drag panning, and click-to-expand.
7. **File opens cleanly** — No console errors, no broken font loads, no layout shifts.
