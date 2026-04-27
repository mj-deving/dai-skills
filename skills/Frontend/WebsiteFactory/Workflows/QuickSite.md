# QuickSite Workflow

Build a professional website in ~15 minutes for ~$5. One-shot with Taste Skill.

## Step 0: Design Pre-Flight (Mandatory)

Before generating any HTML, read the **Core Principles** from `${SKILLS_HOME}/FrontendDesign/SKILL.md`:
- **Design Thinking** — commit to a bold aesthetic direction (purpose, tone, constraints, differentiation)
- **Frontend Aesthetics Guidelines** — typography, color, motion, spatial composition
- **Anti-AI-Slop Rules** — forbidden patterns and required alternatives

These principles apply to ALL website generation. The taste-skill handles CSS-level specifics; FrontendDesign handles design-level thinking.

## Step 1: Gather Requirements

Taste Skill is installed locally at `${SKILLS_HOME}/taste-skill/`. Variants (soft-skill, brutalist-skill, minimalist-skill, redesign-skill, stitch-skill, output-skill) are also available.

Ask the user:
1. What is the website about? (1-2 sentences)
2. What sections do you need? (Hero, About, Projects, Contact — defaults if not specified)
3. Style preference? (dark/light, soft/minimal/brutalist — default: dark + taste-skill core)
4. Any specific content to include? (project names, links, text)

## Step 3: Generate Website

Use the Taste Skill to generate a self-contained HTML file:

```
Use this skill to design a high-end website: https://github.com/Leonxlnx/taste-skill

Design a [USER'S DESCRIPTION] website.

Requirements:
- [FROM USER INPUT]

Style: [USER PREFERENCE or taste-skill default]
DESIGN_VARIANCE: [6 default]
MOTION_INTENSITY: [5 default]  
VISUAL_DENSITY: [4 default]

Output: Single self-contained HTML file with inline CSS and JS.
Responsive. No external dependencies except Google Fonts.
```

## Step 4: Review

1. Open in browser and verify
2. Check mobile responsiveness
3. Iterate 2-3x: "Make the hero text larger", "Mobile optimize", etc.

## Step 5: Optional — Add Video Placeholder

If the user wants animated assets later, add a CSS gradient or particle effect as placeholder:

```
Add an animated CSS gradient background to the hero section as a placeholder.
It should be subtle and professional — we'll replace it with a video later.
```

## Step 6: Deploy (if requested)

Hand off to `Workflows/DeploySite.md` or:

```bash
npx netlify-cli deploy --prod --dir .
```

## Output

- Single `index.html` file (self-contained)
- Responsive, professional design
- Ready for asset integration (Phase 2) or immediate deploy
