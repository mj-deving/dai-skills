---
name: WebsiteFactory
description: Professional website creation workflow — Claude Code + Taste Skill + AI-generated 3D assets (Nano Banana, Seedance, Kling) + Netlify deploy. USE WHEN build website, create website, website factory, portfolio site, landing page, deploy site, taste skill, website with video, animated website, hero video, frontend factory, high-end website, website design.
---

# WebsiteFactory

Professional website creation with AI-generated 3D assets. Two modes: Quick (15 min, ~$5) and Premium (1-2 hrs, ~$10). Produces $5K-$15K agency-level websites.

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/WebsiteFactory/`

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **QuickSite** | "build website", "quick site", "one-shot website", "landing page" | `Workflows/QuickSite.md` |
| **PremiumSite** | "premium website", "brand website", "client website", "portfolio site" | `Workflows/PremiumSite.md` |
| **GenerateAssets** | "generate assets", "hero video", "website animation", "video background" | `Workflows/GenerateAssets.md` |
| **ComponentSourcing** | "source components", "21st.dev", "codepen", "monae", "find components", "component library" | `Workflows/ComponentSourcing.md` |
| **PolishChecklist** | "polish", "craft details", "loading animations", "counter animation", "glassmorphism", "shimmer", "ticker", "scroll progress" | `Workflows/PolishChecklist.md` |
| **VisualEditorLoop** | "visual editor", "stitch redesign", "paper.design", "pencil.dev", "screenshot iterate", "visual iterate" | `Workflows/VisualEditorLoop.md` |
| **WebGLFrontier** | "3D website", "WebGL", "three.js", "threejs", "particles", "3D background", "shader" | `Workflows/WebGLFrontier.md` |
| **BrandedBuild** | "branded page", "mj brand", "portfolio page", "project showcase", "branded prototype", "career page" | `Workflows/BrandedBuild.md` |
| **DeploySite** | "deploy", "make it live", "netlify deploy", "push to netlify" | `Workflows/DeploySite.md` |

## Quick Reference

- **Taste Skill:** `npx skills add Leonxlnx/taste-skill` — [GitHub](https://github.com/Leonxlnx/taste-skill)
- **Nano Banana 2:** Google Gemini 3.1 Flash — images ($0.04-0.15/img)
- **Seedance 2.0:** Video loops via fal.ai API — hero backgrounds (script: `Projekt-Factory/Scripts/seedance-video.py`)
- **Kling 3.0:** 3D product video via fal.ai/klingai — scroll animations
- **Netlify:** Free hosting + CDN — `netlify deploy --prod --dir .`

**Full Workflow Documentation:**
- Detailed spec: `~/projects/KI-Roadmap/Projekt-Factory/Specs/Website-Factory-Workflow.md`
- Portfolio spec: `~/projects/KI-Roadmap/Projekt-Factory/Specs/BA5-Portfolio-Website-Spec.md`

## Design Framework

**Parent skill:** `${SKILLS_HOME}/Frontend/FrontendDesign/SKILL.md` — read Core Principles (Design Thinking, Aesthetics Guidelines, Anti-AI-Slop Rules) before any HTML generation. WebsiteFactory workflows reference this as a mandatory pre-flight.

### Aesthetic Presets (pick ONE)

| Skill | Use For |
|---|---|
| `taste-skill` | Default — core design rules |
| `soft-skill` | Luxury / premium brands |
| `minimalist-skill` | SaaS, dashboards |
| `brutalist-skill` | Creative agencies |
| `redesign-skill` | Upgrading existing sites |

## 3-Dial Parameters

| Parameter | Range | Description |
|---|---|---|
| `DESIGN_VARIANCE` | 1-10 | Layout creativity |
| `MOTION_INTENSITY` | 1-10 | Animation density |
| `VISUAL_DENSITY` | 1-10 | Content per viewport |

## Examples

**Example 1: Quick portfolio site**
```
User: "Build me a portfolio website for my AI automation projects"
→ Invokes QuickSite workflow
→ Installs Taste Skill, generates one-shot HTML
→ Creates placeholder hero (CSS gradient)
→ Responsive, dark theme, professional
```

**Example 2: Premium client website with video**
```
User: "Create a premium website for an architecture firm with animated hero"
→ Invokes PremiumSite workflow
→ Phase 0: Brand Soul + Moodboard + Palette + Logo
→ Phase 1: Claude Code + Taste Skill (soft-skill)
→ Phase 2: Nano Banana hero image → Seedance loop video
→ Phase 3: Integration + optimize + Netlify deploy
```

**Example 3: Generate video assets for existing site**
```
User: "Generate a hero video for my website"
→ Invokes GenerateAssets workflow
→ Guides through Nano Banana → Seedance/Kling pipeline
→ Provides integration prompt for Claude Code
```
