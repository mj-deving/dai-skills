# ComponentSourcing Workflow

Source premium UI components from curated libraries instead of building from scratch. Level 5 — "The Customizer" approach: assemble original designs from high-quality building blocks.

## When to Use

After you have a working site (Levels 1-4) and want to elevate it with polished, interactive components that would take hours to build manually.

## Step 1: Identify What You Need

Review the current site and list components that feel generic or flat:

- Navigation (sticky, animated, mega-menu)
- Hero sections (split, animated text, parallax)
- Buttons (magnetic, morphing, ripple)
- Cards (tilt, flip, glassmorphism)
- Carousels / sliders (3D, infinite scroll)
- Scroll areas (horizontal, parallax sections)
- Maps (interactive, custom markers)
- Hooks (intersection observer, scroll position, mouse tracking)
- Modals / drawers (spring physics, blur backdrop)
- Pricing tables (toggle, highlighted tier)
- Testimonials (marquee, stacked cards)

## Step 2: Source from 21st.dev (Primary)

**URL:** [21st.dev](https://21st.dev)
**What it is:** Curated React/Next.js component library with copy-paste code. High quality, modern animations.

**Workflow:**
1. Browse by category: buttons, navigation, hero, cards, scroll, hooks
2. Preview the component in the live demo
3. Click "Copy Code" — components are self-contained
4. Paste into Claude Code:

```
Here's a component from 21st.dev. Adapt it to match my site's design system:
- Use my color palette: [HEX CODES]
- Use my font: [FONT NAME]
- Adjust sizing to fit my layout
- Keep the animation/interaction behavior

[PASTE COMPONENT CODE]
```

**Best components from 21st.dev:**
- **Magnetic buttons** — cursor-tracking hover effects
- **Animated navbars** — blur-on-scroll, shrink-on-scroll
- **Text reveal** — word-by-word or letter-by-letter entrance
- **Card hover** — tilt effect with 3D perspective transform
- **Scroll hooks** — useScrollProgress, useInView, useMousePosition

## Step 3: Source from CodePen (Secondary)

**URL:** [codepen.io](https://codepen.io)
**What it is:** Massive collection of individual components and effects. Quality varies — use search filters.

**Workflow:**
1. Search for the specific effect: "glassmorphism card CSS", "GSAP scroll animation", "CSS counter animation"
2. Filter by Most Hearted or Most Viewed for quality
3. Open the pen, click "Export" → Download .zip or copy HTML/CSS/JS tabs
4. Paste into Claude Code:

```
Here's a CodePen component I want to integrate into my site.
Extract the core technique and adapt it to my design.
Strip any demo-specific styling and match my palette.

HTML:
[PASTE]

CSS:
[PASTE]

JS:
[PASTE]
```

**Best CodePen searches:**
- "GSAP scroll trigger" — scroll-based animations
- "CSS glassmorphism" — frosted glass cards
- "counter animation" — number count-up effects
- "ticker CSS" — horizontal scrolling text borders
- "shimmer hover" — metallic shine on hover
- "loading animation" — text fade-in, skeleton loaders

## Step 4: Source from Monae (Tertiary)

**URL:** [monae.co](https://monae.co)
**What it is:** Design-focused component library. More opinionated aesthetics than 21st.dev.

**Workflow:**
1. Browse the component gallery
2. Copy the component code
3. Paste into Claude Code with adaptation instructions (same as 21st.dev pattern above)

## Step 5: Integrate and Harmonize

After sourcing 3-5 components, bring them together:

```
I've added these components to my site:
1. [COMPONENT 1] from 21st.dev
2. [COMPONENT 2] from CodePen
3. [COMPONENT 3] from 21st.dev

Now harmonize them:
- Ensure consistent animation timing (spring physics, 0.3-0.5s duration)
- Unify the color usage — accent color only where it matters
- Check that no two components fight for attention
- Mobile: disable heavy animations, simplify interactions
- Performance: use transform/opacity only, no layout thrashing
```

## Component Decision Guide

| Need | Best Source | Why |
|---|---|---|
| React/Next.js components | **21st.dev** | Copy-paste ready, modern stack |
| CSS-only effects | **CodePen** | Largest collection, no framework dependency |
| Design-forward components | **Monae** | Opinionated aesthetics, premium feel |
| GSAP animations | **CodePen** | Most GSAP examples live here |
| Scroll-based interactions | **21st.dev** | Built-in hooks and utilities |
| One-off creative effects | **CodePen** | Widest variety of experimental work |

## Anti-Patterns

- **Don't over-source.** 3-5 sourced components per page max. More than that and the site feels like a component zoo.
- **Don't skip adaptation.** A raw 21st.dev component with its default colors will clash with your design. Always adapt.
- **Don't mix animation libraries.** Pick one: CSS transitions, GSAP, or Framer Motion. Don't use all three on the same page.
- **Don't source what Impeccable can do.** Basic animations (fade-in, slide-up) don't need sourcing — use `Impeccable/animate` instead.
