# VisualEditorLoop Workflow

Level 6 — iterate on design using external visual editors rather than text-only prompting. The key insight: this level is about creative self-expression using Claude as a tool, not riding along.

## When to Use

When text prompting has hit a ceiling. You can describe what you want but Claude keeps producing variations that aren't quite right. Visual editors let you show rather than tell.

## The Core Loop

```
1. Screenshot current site state
2. Drop into visual editor (Stitch / Paper.design / Pencil.dev)
3. Generate redesign variants or edit visually
4. Copy/export the variant you like best
5. Bring back to Claude Code as visual reference
6. "Match this design direction"
7. Claude implements + searches best practices
8. Repeat until satisfied
```

## Visual Editor Options

### Google Stitch (Primary — Free)

**URL:** [labs.google.com/stitch](https://labs.google.com/stitch)

**What it does:** Visual canvas powered by Gemini. Upload screenshots, generate redesign variants, drag elements, change layouts visually.

**Workflow:**
1. Screenshot your current site (full page or specific section)
2. Upload to Stitch
3. Describe the change: "Make the hero section more dramatic" or "Redesign this pricing section with a dark theme"
4. Stitch generates 2-4 visual variants
5. Pick the best one
6. Right-click → Copy Image (or screenshot the variant)
7. Paste into Claude Code:

```
Here's a design direction from Google Stitch.
Match this visual style for my [SECTION NAME]:
- Layout structure
- Color usage and contrast
- Typography sizing and weight
- Spacing and whitespace

Don't copy it pixel-perfect — adapt it to my existing design system.
My palette: [HEX CODES]
My font: [FONT NAME]

[PASTE SCREENSHOT]
```

**Best for:** Rapid visual exploration, trying completely different layouts, getting unstuck when you can't articulate what you want.

**Integration with stitch-skill:** If you want Stitch to maintain consistency across screens, first generate a DESIGN.md using `Aesthetics/stitch-skill`, then upload it to Stitch as a design system reference.

### Paper.design (Secondary)

**URL:** [paper.design](https://paper.design)

**What it does:** Browser-based visual editor for designing web pages. More hands-on than Stitch — you're directly manipulating elements rather than generating variants.

**Workflow:**
1. Start a new project or import your current site's HTML
2. Edit visually: drag elements, change colors, adjust spacing
3. Export the design as an image or code snippet
4. Bring to Claude Code for implementation

**Best for:** When you know roughly what you want and need fine visual control. Good for layout iteration.

### Pencil.dev (Tertiary — IDE Integration)

**URL:** [pencil.dev](https://pencil.dev)

**What it does:** Visual editor that integrates with Cursor and VS Code. Real-time canvas editing alongside your code.

**Workflow:**
1. Install the Pencil extension in your IDE
2. Open your project — Pencil renders a live visual canvas
3. Edit visually: the canvas writes code back to your files
4. Switch to Claude Code for logic/animation/polish that Pencil can't do visually

**Best for:** When you want to stay in the IDE. Good for component-level visual tweaking.

## The Web Search Pattern

When Claude Code implements a visual direction but the result isn't quite right, use targeted web search:

```
Web search best practices for [SPECIFIC EFFECT].
Then implement the best approach for my site.

Examples:
- "best web design practices for card hover effects"
- "modern hero section scroll animation techniques 2026"
- "glassmorphism implementation with backdrop-filter performance"
- "GSAP ScrollTrigger pinning best practices"
```

This is what separates Level 6 from Level 5 — you're actively directing the design process and using Claude to research solutions rather than hoping it guesses right.

## Decision Guide

| Situation | Editor | Why |
|---|---|---|
| "I don't know what I want" | **Stitch** | Generates variants for you to react to |
| "I know the layout, need to refine" | **Paper.design** | Direct visual manipulation |
| "I want to tweak components in-IDE" | **Pencil.dev** | Code ↔ canvas sync |
| "The effect isn't right" | **Web Search** | Research best practices, not more guessing |
| "I need consistent multi-page design" | **Stitch + stitch-skill** | DESIGN.md ensures consistency |

## Tips for Effective Visual Iteration

1. **Screenshot before and after each iteration.** Build a visual history. This helps you and Claude understand what's improving.
2. **Be specific about what you like in a variant.** "I like the spacing in variant 2 but the color treatment in variant 3" is much more useful than "combine these."
3. **Don't start from scratch each time.** Build on what's working. Change one thing per iteration.
4. **Name your design decisions.** "The hero uses a split layout because we need text and image side-by-side" — this prevents Claude from redesigning things you've already decided on.
5. **Use web search for technique names.** Once you see an effect you like, search for its name ("parallax scrolling", "morph transition", "staggered grid reveal") — having the right vocabulary makes prompting dramatically more effective.

## Relationship to Other Workflows

- **stitch-skill** (Aesthetics) — generates DESIGN.md files for Stitch. Use it to establish design system rules before entering the visual editor loop.
- **GenerateAssets** — creates AI images/videos. Use the visual editor loop to decide placement and integration style for those assets.
- **PolishChecklist** — specific techniques to apply after the visual editor loop converges on a direction.
