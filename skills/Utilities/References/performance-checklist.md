---
name: Performance Checklist
description: Core Web Vitals targets, frontend/backend optimization checklists, common anti-patterns. USE WHEN building HTML output, optimizing frontend, reviewing performance, checking Web Vitals, N+1 queries, bundle size.
source: addyosmani/agent-skills (MIT) — adapted for PAI reference
---

# Performance Checklist

Quick reference for web application performance. Consult when building or reviewing any frontend output (VisualExplainer, ScientificDeck-HTML, Cloudflare Pages).

## Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

## TTFB Diagnosis

When TTFB is slow (> 800ms), check DevTools Network waterfall:

- [ ] **DNS resolution** slow → `<link rel="dns-prefetch">` or `<link rel="preconnect">`
- [ ] **TCP/TLS handshake** slow → enable HTTP/2, consider edge deployment
- [ ] **Server processing** slow → profile backend, check slow queries, add caching

## Frontend Checklist

### Images
- [ ] Modern formats (WebP, AVIF)
- [ ] Responsively sized (`srcset` and `sizes`)
- [ ] Explicit `width` and `height` (prevents CLS)
- [ ] Below-fold: `loading="lazy"` + `decoding="async"`
- [ ] Hero/LCP: `fetchpriority="high"`, no lazy loading

### JavaScript
- [ ] Bundle under 200KB gzipped (initial load)
- [ ] Code splitting with dynamic `import()` for routes
- [ ] Tree shaking enabled (ESM + `sideEffects: false`)
- [ ] No blocking JS in `<head>` (use `defer` or `async`)
- [ ] Heavy computation → Web Workers
- [ ] `React.memo()` only where profiling shows benefit
- [ ] `useMemo()`/`useCallback()` only where profiling shows benefit

### CSS
- [ ] Critical CSS inlined or preloaded
- [ ] No render-blocking CSS for non-critical styles
- [ ] No CSS-in-JS runtime cost in production
- [ ] `font-display: swap` or `optional`
- [ ] System font stack considered before custom fonts

### Network
- [ ] Static assets: long `max-age` + content hashing
- [ ] API responses cached where appropriate
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] `<link rel="preconnect">` for known origins
- [ ] No unnecessary redirects

### Rendering
- [ ] No layout thrashing (batch DOM reads, then writes)
- [ ] Animations use `transform` and `opacity` (GPU-accelerated)
- [ ] Long lists virtualized (e.g., `react-window`)
- [ ] No unnecessary full-page re-renders

## Backend Checklist

### Database
- [ ] No N+1 query patterns (use eager loading / joins)
- [ ] Queries have appropriate indexes
- [ ] List endpoints paginated (never unbounded SELECT)
- [ ] Connection pooling configured
- [ ] Slow query logging enabled

### API
- [ ] Response times < 200ms (p95)
- [ ] No synchronous heavy computation in request handlers
- [ ] Bulk operations instead of loops
- [ ] Response compression (gzip/brotli)
- [ ] Appropriate caching (in-memory, Redis, CDN)

## Measurement Commands

```bash
# Lighthouse CLI
npx lighthouse https://localhost:3000 --output json --output-path ./report.json

# Bundle analysis (webpack)
npx webpack-bundle-analyzer stats.json
# Bundle analysis (Vite)
npx vite-bundle-visualizer

# Web Vitals in code
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(console.log); onINP(console.log); onCLS(console.log);
```

## Common Anti-Patterns

| Anti-Pattern | Impact | Fix |
|---|---|---|
| N+1 queries | Linear DB load growth | Joins, includes, batch loading |
| Unbounded queries | Memory exhaustion, timeouts | Always paginate, add LIMIT |
| Missing indexes | Slow reads as data grows | Index filtered/sorted columns |
| Layout thrashing | Jank, dropped frames | Batch DOM reads, then writes |
| Unoptimized images | Slow LCP, wasted bandwidth | WebP, responsive sizes, lazy load |
| Large bundles | Slow Time to Interactive | Code split, tree shake, audit deps |
| Blocking main thread | Poor INP, unresponsive UI | Web Workers, defer work |
| Memory leaks | Growing memory, eventual crash | Clean up listeners, intervals, refs |
