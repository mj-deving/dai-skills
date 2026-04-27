---
name: UIUXProMax
description: Data-driven UI/UX design intelligence — 67 styles, 161 palettes, 57 font pairings, 25 chart types, 99 UX guidelines across 16 tech stacks. Python search tool for context-aware design recommendations. USE WHEN design system, color palette, font pairing, style selection, UX guidelines, chart design, design review, UI audit, landing page design, dashboard design, SaaS design, glassmorphism, claymorphism, brutalism, neumorphism, bento grid, dark mode, responsive design, product type design, design intelligence, pro max.
---

# UI/UX Pro Max — Design Intelligence

Comprehensive design guide with searchable database. 67 styles, 161 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 16 technology stacks. Priority-based recommendations with reasoning rules.

Source: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

## Usage

### Generate Design System (primary workflow)

```bash
python3 ${SKILLS_HOME}/Frontend/UIUXProMax/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

Returns: complete design system with pattern, style, colors, typography, effects + anti-patterns to avoid.

### Search Specific Domains

```bash
python3 ${SKILLS_HOME}/Frontend/UIUXProMax/scripts/search.py "<query>" --domain <domain>
```

Domains: `style`, `color`, `typography`, `ux`, `landing`, `product`, `chart`, `react`, `icons`, `app-interface`

### Stack-Specific Best Practices

```bash
python3 ${SKILLS_HOME}/Frontend/UIUXProMax/scripts/search.py "<query>" --stack <stack>
```

Stacks: react, nextjs, vue, nuxtjs, nuxt-ui, svelte, astro, html-tailwind, shadcn, swiftui, react-native, flutter, jetpack-compose, threejs, angular, laravel

### Persist Design System

```bash
python3 ${SKILLS_HOME}/Frontend/UIUXProMax/scripts/search.py "<query>" --design-system --persist
```

Saves to `.ui-ux-pro-max/DESIGN_SYSTEM.md` for cross-session retrieval.

## Data Files

| File | Records | Content |
|---|---|---|
| `data/design.csv` | 1,775 | Core design rules + reasoning |
| `data/google-fonts.csv` | 1,924 | Font pairings with usage context |
| `data/draft.csv` | 1,778 | Draft/extended rules |
| `data/products.csv` | 162 | Product type → design pattern mapping |
| `data/colors.csv` | 161 | Color palettes by industry/mood |
| `data/ui-reasoning.csv` | 162 | Why-rules for style selection |
| `data/icons.csv` | 105 | Icon library recommendations |
| `data/ux-guidelines.csv` | 99 | UX rules by priority |
| `data/styles.csv` | 85 | Style definitions (glass, clay, etc.) |
| `data/typography.csv` | 74 | Typography scale + pairing rules |
| `data/stacks/*.csv` | ~50 each | Per-framework best practices |

## Quick Reference

See `templates/base/quick-reference.md` for the full 300+ rule checklist across 10 categories:
1. Accessibility (CRITICAL)
2. Touch & Interaction (CRITICAL)
3. Performance (HIGH)
4. Style Selection (HIGH)
5. Layout & Responsive (HIGH)
6. Typography & Color (MEDIUM)
7. Animation (MEDIUM)
8. Forms & Feedback (MEDIUM)
9. Navigation Patterns (HIGH)
10. Charts & Data (LOW)
