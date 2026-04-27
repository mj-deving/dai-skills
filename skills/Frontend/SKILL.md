---
name: Frontend
description: Frontend design and website engineering — standards, anti-slop rules, aesthetic presets, website factory, design intelligence, audit commands, and site teardown. USE WHEN building UI, HTML, frontend, design review, responsive, website factory, portfolio site, landing page, impeccable, audit, typeset, animate, colorize, critique, layout, polish, delight, harden, site teardown, clone website, redesign.
---

# Frontend

Unified skill for frontend design, website engineering, and visual quality. Covers the full spectrum from anti-slop standards through aesthetic presets to production website workflows.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| **Standards & Review** | |
| Design review, review UI, check accessibility, review frontend, anti-slop check, component architecture | `FrontendDesign/SKILL.md` |
| **Website Building** | |
| Build website, create website, landing page, portfolio site, deploy, netlify, quick site, premium site, generate assets, hero video, source components, 21st.dev, codepen, monae, polish, craft details, visual editor, stitch redesign, paper.design, pencil.dev, 3D website, WebGL, three.js, particles, shader | `WebsiteFactory/SKILL.md` |
| Branded page, MJ brand build, project showcase, portfolio page, career page, branded prototype | `WebsiteFactory/SKILL.md` → BrandedBuild |
| **Presentations** | |
| Create slides, presentation, convert PPTX, frontend slides, slide deck | `frontend-slides/SKILL.md` |
| **Design Intelligence** | |
| Design system generation, color palette, font pairing, style for industry, UX guidelines, product type design, chart design, pro max | `UIUXProMax/SKILL.md` |
| **Audit & Craft Commands (Impeccable)** | |
| Impeccable, craft, teach, extract design system | `Impeccable/impeccable/SKILL.md` |
| Audit, accessibility audit, performance audit, quality check | `Impeccable/audit/SKILL.md` |
| Deep accessibility, WCAG deep dive, a11y-deep, full WCAG audit, accessibility specialists | `Impeccable/a11y-deep/SKILL.md` |
| Typography, typeset, font scale, font pairing, type hierarchy | `Impeccable/typeset/SKILL.md` |
| Animate, motion, transitions, scroll animations, micro-interactions | `Impeccable/animate/SKILL.md` |
| Colorize, color system, palette, contrast, themes | `Impeccable/colorize/SKILL.md` |
| Critique, design critique, review with overlay | `Impeccable/critique/SKILL.md` |
| Layout, arrange, grid, flexbox, spatial composition | `Impeccable/layout/SKILL.md` |
| Polish, normalize, clean up, CSS quality | `Impeccable/polish/SKILL.md` |
| Shape, visual structure, composition, hierarchy | `Impeccable/shape/SKILL.md` |
| Delight, micro-delight, surprise, premium feel | `Impeccable/delight/SKILL.md` |
| Harden, production-ready, cross-browser, edge cases | `Impeccable/harden/SKILL.md` |
| Optimize, performance, bundle, rendering, paint | `Impeccable/optimize/SKILL.md` |
| Adapt, responsive, breakpoints, mobile, tablet | `Impeccable/adapt/SKILL.md` |
| Bolder, more dramatic, stronger contrast, louder | `Impeccable/bolder/SKILL.md` |
| Clarify, simplify UI, reduce noise, clean interface | `Impeccable/clarify/SKILL.md` |
| Distill, extract tokens, design tokens, CSS variables | `Impeccable/distill/SKILL.md` |
| Overdrive, maximum polish, final pass, ship-ready | `Impeccable/overdrive/SKILL.md` |
| Quieter, subtle, restrained, reduce visual noise | `Impeccable/quieter/SKILL.md` |
| **Aesthetic Presets** (pick ONE per project) | |
| Premium metric-based, GSAP, ThreeJS, bento grids | `Aesthetics/taste-skill/SKILL.md` |
| Luxury agency, expensive shadows, premium feel | `Aesthetics/soft-skill/SKILL.md` |
| Industrial raw, Swiss typography, military terminal | `Aesthetics/brutalist-skill/SKILL.md` |
| Editorial clean, warm monochrome, muted pastels | `Aesthetics/minimalist-skill/SKILL.md` |
| Upgrade existing site, audit + fix in-place | `Aesthetics/redesign-skill/SKILL.md` |
| Google Stitch design system, DESIGN.md generation | `Aesthetics/stitch-skill/SKILL.md` |
| Brand design reference, "like Stripe", "like Apple", design inspiration, getdesign, brand style | `Aesthetics/brand-references/SKILL.md` |

## Architecture

```
Frontend/
├── FrontendDesign/          ← Standards hub (anti-slop, a11y, component patterns)
├── WebsiteFactory/          ← Build workflows (Quick/Premium/Assets/Deploy)
├── frontend-slides/         ← HTML presentations
├── UIUXProMax/              ← Data-driven design search (161 palettes, 57 fonts, 16 stacks)
├── Impeccable/              ← 18 audit/craft commands (typeset, animate, colorize, etc.)
│   ├── impeccable/          ← Main entry (craft/teach/extract)
│   ├── audit/               ← Technical quality checks
│   ├── typeset/             ← Typography
│   ├── animate/             ← Motion & transitions
│   ├── colorize/            ← Color systems
│   ├── critique/            ← Design critique with overlay
│   ├── layout/              ← Spatial composition
│   ├── polish/              ← CSS cleanup & normalization
│   ├── shape/               ← Visual structure
│   ├── delight/             ← Micro-interactions & premium feel
│   ├── harden/              ← Production hardening
│   ├── optimize/            ← Performance
│   ├── adapt/               ← Responsive design
│   ├── bolder/              ← Increase drama/contrast
│   ├── clarify/             ← Simplify & reduce noise
│   ├── distill/             ← Extract design tokens
│   ├── overdrive/           ← Final polish pass
│   └── quieter/             ← Reduce visual intensity
└── Aesthetics/              ← CSS-level aesthetic presets
    ├── taste-skill/
    ├── soft-skill/
    ├── brutalist-skill/
    ├── minimalist-skill/
    ├── redesign-skill/
    ├── brand-references/     ← 7 bundled + 69 fetchable brand DESIGN.md files
    └── stitch-skill/
```

## Recommended Workflow (7-Level Progression)

Based on "7 Levels of Elite Websites with Claude Code":

1. **Standards** — `FrontendDesign/` anti-slop rules + plan mode (Level 1-2)
2. **Design Intelligence** — `UIUXProMax/` for data-driven design system generation (Level 2)
3. **Aesthetic Preset** — Pick ONE from `Aesthetics/` matching your project tone (Level 2)
4. **Audit** — `Impeccable/audit/` for systematic quality check (Level 2)
5. **Visual References** — Screenshots from Awwwards/Godly/Pinterest (Level 3)
6. **Site Teardown** — Ctrl+U → HTML/CSS/JS extraction from reference sites (Level 4)
7. **Components** — `WebsiteFactory/` ComponentSourcing from 21st.dev, CodePen, Monae (Level 5)
8. **Custom Assets** — `WebsiteFactory/` GenerateAssets workflow for AI art/video (Level 5)
9. **Polish** — `WebsiteFactory/` PolishChecklist for craft details: loading anims, counters, glassmorphism, shimmer, tickers (Level 5)
10. **Iterate** — `Impeccable/` commands for targeted refinement (Level 5)
11. **Visual Editor Loop** — `WebsiteFactory/` VisualEditorLoop with Stitch/Paper.design/Pencil.dev (Level 6)
12. **Ship** — `Impeccable/overdrive/` + `WebsiteFactory/` DeploySite (Level 6)
13. **3D Frontier** — `WebsiteFactory/` WebGLFrontier for Three.js/WebGL experiences (Level 7, aspirational)

## Examples

**Example 1:** `User: "[typical request]"` → Routes to appropriate sub-skill workflow

**Example 2:** `User: "[another request]"` → Routes to different sub-skill workflow
