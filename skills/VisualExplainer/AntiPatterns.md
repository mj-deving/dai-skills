# Anti-Patterns (AI Slop)

These patterns are explicitly forbidden. They signal "AI-generated template" and undermine the skill's purpose.

## Typography
**Forbidden as primary `--font-body`:** Inter, Roboto, Arial, Helvetica, system-ui alone.
**Required:** Pick from font pairings in `Libraries.md`. Every generation uses a different pairing.

## Color Palette
**Forbidden accent colors:** `#8b5cf6`, `#7c3aed`, `#a78bfa` (indigo/violet), `#d946ef` (fuchsia), cyan+magenta+pink neon gradient.
**Forbidden effects:** Gradient text on headings (`background-clip: text`), animated glowing box-shadows, multiple overlapping radial glows.
**Required:** Build palettes from terracotta/sage, teal/cyan, rose/cranberry, slate/blue, or real IDE themes (Dracula, Nord, Solarized, Gruvbox, Catppuccin).

## Section Headers
**Forbidden:** Emoji icons in headers, identical icon-in-rounded-box pattern across sections.
**Required:** Styled monospace labels with colored dot indicators, numbered badges, or asymmetric dividers.

## Layout & Hierarchy
**Forbidden:** Perfectly centered everything, all identical cards, symmetric layouts, equal visual treatment for all sections.
**Required:** Vary visual weight. Hero sections dominate. Reference sections stay compact. Use depth tiers.

## Template Patterns
**Forbidden:** Three-dot window chrome, identical gradient KPIs, neon dashboard aesthetic, gradient mesh backgrounds.
**Required:** Simple code block headers, varied KPI treatment, constrained aesthetics (Blueprint, Editorial, Paper/ink).

## The Slop Test (7 Points)
If 2+ of these are present, regenerate with a constrained aesthetic:
1. Inter or Roboto font with purple/violet gradient accents
2. Every heading has `background-clip: text` gradient
3. Emoji icons leading every section
4. Glowing cards with animated shadows
5. Cyan-magenta-pink color scheme on dark background
6. Perfectly uniform card grid with no visual hierarchy
7. Three-dot code block chrome
