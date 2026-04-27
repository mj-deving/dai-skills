---
name: DesignReview
description: Structured frontend design review — 5-axis evaluation with verification checklist
---

# Design Review Workflow

Structured review of frontend UI output across 5 axes.

## When to Use

- After building UI components or pages
- Before shipping frontend changes
- When the user asks "review the design" or "check accessibility"
- Invoked by Designer agent during review cycles

## Process

### Step 1: Load References

Read the relevant reference files based on what's being reviewed:
- `ComponentPatterns.md` — anti-slop rules, design thinking, architecture
- `AccessibilityGuidelines.md` — WCAG 2.1 AA, code patterns
- `ResponsivePatterns.md` — breakpoints, viewport fitting
- `${SKILLS_HOME}/Utilities/References/performance-checklist.md` — Core Web Vitals
- `${SKILLS_HOME}/Utilities/References/accessibility-checklist.md` — quick checklist

### Step 2: 5-Axis Review

Evaluate the UI across these five dimensions:

**1. Visual Quality & Anti-Slop**
- Does it look like a real product or AI-generated?
- Check against anti-AI-slop table in ComponentPatterns.md
- Typography: distinctive and appropriate, not Inter/Roboto/Arial?
- Color: intentional palette or generic purple gradient?
- Spacing: consistent scale or arbitrary pixel values?
- Layout: purposeful or stock template?

**2. Accessibility (WCAG 2.1 AA)**
- Keyboard: can you Tab through everything?
- Screen reader: all images have alt, inputs have labels, headings don't skip?
- Contrast: text >= 4.5:1, UI components >= 3:1?
- Color not sole indicator of state?
- Focus indicators visible?

**3. Responsiveness**
- Works at 320px, 768px, 1024px, 1440px?
- Touch targets >= 44x44px on mobile?
- No horizontal scroll?
- Images don't overflow?

**4. Component Architecture**
- Components under 200 lines?
- Data fetching separated from presentation?
- Loading, error, and empty states handled?
- State management appropriate (simplest tool that works)?

**5. Performance**
- Images optimized (WebP, srcset, lazy loading)?
- No layout thrashing?
- Bundle implications considered?
- Core Web Vitals would pass?

### Step 3: Classify Findings

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | Blocks shipping — accessibility failure, broken at common viewport | Fix before merge |
| **Important** | Should fix — anti-slop violation, missing state, poor contrast | Fix in this PR |
| **Nit** | Nice to have — spacing refinement, font choice | Optional |

### Step 4: Output

```markdown
## Design Review

### Overall Assessment
[One paragraph — professional quality? AI-slop detected? Accessible?]

### Findings
[List each finding with severity, file:line, and specific recommendation]

### Verification Checklist
- [ ] Renders without console errors
- [ ] All interactive elements keyboard accessible
- [ ] Screen reader can convey structure
- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] Loading, error, empty states handled
- [ ] Follows design system (spacing, colors, typography)
- [ ] No AI-slop patterns detected
- [ ] No accessibility warnings (axe-core)
```
