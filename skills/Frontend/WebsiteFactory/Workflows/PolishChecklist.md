# PolishChecklist Workflow

Level 5 craft details that transform a functional site into a cohesive, premium experience. These are the "little things that most people won't notice — when combined, create something that looks coherent and crafted."

## When to Use

After the site works and looks good (Levels 1-4 complete, components sourced). This is the final craft pass before deploying.

## The Checklist

Work through each category. Skip what doesn't apply to your project.

### Loading & Entrance

- [ ] **Text fade-in on load** — Headlines and body text fade in with slight upward motion (0.3s ease-out, 20px translate). Gives text visual "weight" instead of instant pop.
- [ ] **Staggered section reveal** — Each section enters sequentially as user scrolls. Cascade delay: 0.1s between elements within a section.
- [ ] **Skeleton loaders** — For any content that loads asynchronously, show shaped placeholders matching the final layout. No circular spinners.
- [ ] **Image lazy loading** — Below-fold images load on scroll approach. Use `loading="lazy"` or Intersection Observer for custom timing.

### Typography Polish

- [ ] **Custom Google Font** — Replace system fonts with a distinctive typeface. Impact is immediate and massive. See UIUXProMax for pairing recommendations.
- [ ] **Headline tracking** — Tighten letter-spacing on large headlines (-0.02em to -0.04em). Looser tracking on small text (+0.01em).
- [ ] **Responsive font sizing** — Use `clamp()` for fluid type: `clamp(2rem, 5vw, 4rem)` for headlines.
- [ ] **Max line width** — Body text at 65ch max-width. Prevents eye fatigue on wide screens.

### Scroll Interactions

- [ ] **Scroll progress bar** — Thin bar (2-3px) at the top of the viewport showing scroll position. Accent color. CSS-only or minimal JS.

```css
/* CSS-only scroll progress */
body {
  background: linear-gradient(to right, var(--accent) var(--scroll), transparent 0);
  background-size: 100% 3px;
  background-repeat: no-repeat;
  background-position: top;
}
```

- [ ] **Parallax sections** — Background elements move at 0.3-0.5x scroll speed. Foreground at 1x. Subtle depth without nausea.
- [ ] **Scroll-triggered counters** — Numbers animate from 0 to target value when they enter viewport. Duration: 1.5-2s. Use `Intl.NumberFormat` for commas.

```javascript
// Counter animation pattern
function animateCounter(element, target, duration = 2000) {
  const start = performance.now();
  const update = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    element.textContent = Math.floor(target * eased).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}
```

### Visual Effects

- [ ] **Glassmorphism cards** — Semi-transparent background with backdrop blur. Use sparingly (1-2 elements per page).

```css
.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 1rem;
}
```

- [ ] **Hover shimmer effect** — Metallic shine sweep on card/button hover. CSS gradient animation.

```css
.shimmer:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    transparent 25%,
    rgba(255, 255, 255, 0.15) 50%,
    transparent 75%
  );
  animation: shimmer 0.6s ease-in-out;
}
@keyframes shimmer {
  from { transform: translateX(-100%); }
  to { transform: translateX(100%); }
}
```

- [ ] **Ticker borders** — Horizontal scrolling text between sections. Infinite CSS animation. Good for social proof or feature lists.

```css
.ticker {
  overflow: hidden;
  white-space: nowrap;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 0;
}
.ticker-inner {
  display: inline-flex;
  gap: 2rem;
  animation: ticker 20s linear infinite;
}
@keyframes ticker {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}
```

- [ ] **Gradient mesh backgrounds** — Subtle, multi-stop radial gradients as section backgrounds. Not solid colors, not linear gradients.

### Micro-Interactions

- [ ] **Button press feedback** — `transform: translateY(1px)` on `:active`. Tactile, physical feel.
- [ ] **Link hover underline** — Animated underline that slides in from left on hover, not instant toggle.
- [ ] **Focus ring styling** — Custom focus ring using `box-shadow` with accent color. Visible but not ugly.
- [ ] **Cursor changes** — `cursor: pointer` on all clickable elements. No custom cursor shapes.
- [ ] **Form input transitions** — Border color and label position transition smoothly on focus (0.2s ease).

### Performance Guards

- [ ] **Video fallback** — Desktop: video hero. Mobile: static image. Check `prefers-reduced-motion` media query.
- [ ] **Animation budget** — No more than 3 simultaneous animations in viewport at any time.
- [ ] **Transform-only animations** — Every animation uses `transform` and `opacity` only. Never animate `width`, `height`, `top`, `left`, `margin`, `padding`.
- [ ] **Font loading** — `font-display: swap` on all custom fonts. Optional: preload the primary headline font.

## Usage with Claude Code

```
Run through the Polish Checklist on my site.
Current state: [DESCRIBE]
Priority: [loading animations / scroll effects / visual effects / all]
Accent color: [HEX]
Constraint: keep it performant on mobile.
```

## Relationship to Impeccable

This checklist focuses on **specific Level 5 techniques** from the 7-Levels progression. For broader quality passes, use:
- `Impeccable/delight` — general micro-interactions and premium feel
- `Impeccable/animate` — motion system and transitions
- `Impeccable/polish` — CSS cleanup and normalization
- `Impeccable/overdrive` — final ship-ready pass
