---
name: Responsive Patterns
description: Mobile-first responsive design patterns, breakpoints, viewport fitting, content density, and Tailwind patterns
source: addyosmani/agent-skills frontend-ui-engineering (MIT), zarazhangrui/frontend-slides
---

# Responsive Design Patterns

## Mobile-First Approach

Start with smallest viewport, enhance upward. Never desktop-first.

```tsx
// Tailwind: mobile-first responsive
<div className="
  grid grid-cols-1      /* Mobile: single column */
  sm:grid-cols-2        /* Small: 2 columns */
  lg:grid-cols-3        /* Large: 3 columns */
  gap-4
">
```

## Breakpoints

| Breakpoint | Target | Priority | Tailwind |
|-----------|--------|----------|----------|
| 320px | Small phone | Must work | (default) |
| 640px | Large phone | Should work | `sm:` |
| 768px | Tablet | Must work | `md:` |
| 1024px | Laptop | Must work | `lg:` |
| 1440px | Desktop | Should work | `xl:` |

**Always test at 320px** — this is the minimum viable viewport. If it works here, it works everywhere larger.

## Layout Patterns

### Stack → Grid Transition
```tsx
// Stack on mobile, side-by-side on tablet+
<div className="flex flex-col md:flex-row gap-4">
  <aside className="md:w-64 shrink-0">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>
```

### Responsive Typography
```css
/* Use clamp() for fluid type scaling */
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }
h2 { font-size: clamp(1.25rem, 3vw, 2rem); }
body { font-size: clamp(0.875rem, 1.5vw, 1rem); }
```

### Container Queries (modern approach)
```css
/* Size based on container, not viewport */
@container (min-width: 400px) {
  .card { flex-direction: row; }
}
```

## Viewport Fitting (from zarazhangrui/frontend-slides)

For single-screen content (dashboards, slides, presentations):

- Content should fill the viewport without requiring scroll where possible
- Use `100dvh` (dynamic viewport height) not `100vh` (static, problematic on mobile)
- Fit content to viewport with `object-fit: contain` for media
- Consider scroll-snap for multi-section layouts

```css
.slide {
  height: 100dvh;
  scroll-snap-align: start;
  display: grid;
  place-items: center;
  padding: clamp(1rem, 4vw, 3rem);
}
```

## Content Density (from zarazhangrui/frontend-slides)

- **Compact**: Dense information, smaller text, tight spacing — for data-heavy dashboards
- **Normal**: Standard spacing and sizing — for most applications
- **Spacious**: Generous whitespace, larger text — for marketing/landing pages

```css
/* CSS custom properties for density control */
:root {
  --density-spacing: 1rem;    /* normal */
  --density-text: 1rem;
}
[data-density="compact"] {
  --density-spacing: 0.5rem;
  --density-text: 0.875rem;
}
[data-density="spacious"] {
  --density-spacing: 1.5rem;
  --density-text: 1.125rem;
}
```

- Limit content per section: 3-5 key points, not walls of text
- Visual hierarchy through typography scale, not color alone
- White space is a feature, not wasted space — but must be intentional

## Touch Targets

- Minimum 44x44px on mobile (WCAG 2.5.8)
- Spacing between targets >= 8px to prevent accidental taps
- Links in body text: increase line-height to make tap targets larger

```tsx
// Good: adequate touch target
<button className="min-h-[44px] min-w-[44px] p-3">
  <TrashIcon className="h-5 w-5" />
</button>

// Bad: tiny icon button
<button className="p-1">
  <TrashIcon className="h-4 w-4" />
</button>
```

## Images

- Always set explicit `width` and `height` (prevents CLS)
- Use `srcset` for responsive sizes
- Below fold: `loading="lazy"` + `decoding="async"`
- Hero/LCP: `fetchpriority="high"`, NO lazy loading
- Modern formats: WebP, AVIF with fallback

```html
<img
  src="photo.webp"
  srcset="photo-320.webp 320w, photo-768.webp 768w, photo-1440.webp 1440w"
  sizes="(max-width: 768px) 100vw, 50vw"
  width="1440" height="960"
  loading="lazy" decoding="async"
  alt="Descriptive alt text"
/>
```

## Testing Checklist

- [ ] Works at 320px (small phone)
- [ ] Works at 768px (tablet)
- [ ] Works at 1024px (laptop)
- [ ] Works at 1440px (desktop)
- [ ] Touch targets >= 44x44px on mobile
- [ ] No horizontal scroll at any breakpoint
- [ ] Text readable without zoom at all sizes
- [ ] Images don't overflow containers
- [ ] Navigation accessible at all breakpoints
