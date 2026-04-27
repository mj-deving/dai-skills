---
name: Accessibility Checklist
description: WCAG 2.1 AA compliance reference — keyboard nav, screen readers, color contrast, forms, ARIA patterns. USE WHEN generating HTML (VisualExplainer, ScientificDeck-HTML), building UI, reviewing accessibility, checking WCAG compliance.
source: addyosmani/agent-skills (MIT) — adapted for PAI reference
---

# Accessibility Checklist

Quick reference for WCAG 2.1 AA compliance. Consult when generating any HTML output (VisualExplainer, ScientificDeck-HTML, Cloudflare Pages, any UI work).

## Essential Checks

### Keyboard Navigation
- [ ] All interactive elements focusable via Tab
- [ ] Focus order follows visual/logical order
- [ ] Focus is visible (outline/ring on focused elements)
- [ ] Custom widgets: Enter to activate, Escape to close
- [ ] No keyboard traps (can always Tab away)
- [ ] Skip-to-content link at top of page
- [ ] Modals trap focus while open, return focus on close

### Screen Readers
- [ ] All images have `alt` text (or `alt=""` for decorative)
- [ ] All form inputs have associated labels (`<label>` or `aria-label`)
- [ ] Buttons and links have descriptive text (not "Click here")
- [ ] Icon-only buttons have `aria-label`
- [ ] One `<h1>` per page, headings don't skip levels
- [ ] Dynamic content announced (`aria-live` regions)
- [ ] Tables have `<th>` headers with scope

### Visual
- [ ] Text contrast >= 4.5:1 (normal) or >= 3:1 (large, 18px+)
- [ ] UI component contrast >= 3:1 against background
- [ ] Color is NOT the only way to convey information
- [ ] Text resizable to 200% without breaking layout
- [ ] No content flashing > 3 times per second

### Forms
- [ ] Every input has a visible label
- [ ] Required fields indicated (not by color alone)
- [ ] Error messages specific and associated with field
- [ ] Error state visible by more than color (icon, text, border)
- [ ] Form submission errors summarized and focusable

### Content
- [ ] Language declared (`<html lang="en">`)
- [ ] Page has descriptive `<title>`
- [ ] Links distinguish from surrounding text (not by color alone)
- [ ] Touch targets >= 44x44px on mobile
- [ ] Meaningful empty states (not blank screens)

## Common HTML Patterns

### Buttons vs Links

```html
<!-- Use <button> for actions -->
<button onClick={handleDelete}>Delete Task</button>

<!-- Use <a> for navigation -->
<a href="/tasks/123">View Task</a>

<!-- NEVER use div/span as buttons -->
<div onClick={handleDelete}>Delete</div>  <!-- BAD: not focusable, no keyboard -->
```

### Form Labels

```html
<!-- Explicit association (preferred) -->
<label htmlFor="email">Email address</label>
<input id="email" type="email" required />

<!-- Implicit wrapping -->
<label>
  Email address
  <input type="email" required />
</label>

<!-- Hidden label (visible label preferred) -->
<input type="search" aria-label="Search tasks" />
```

### ARIA Roles

```html
<!-- Navigation -->
<nav aria-label="Main navigation">...</nav>

<!-- Status messages -->
<div role="status" aria-live="polite">Task saved</div>

<!-- Alert messages -->
<div role="alert">Error: Title is required</div>

<!-- Modal dialogs -->
<dialog aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm Delete</h2>
</dialog>

<!-- Loading states -->
<div aria-busy="true" aria-label="Loading tasks">
  <Spinner />
</div>
```

## ARIA Live Regions Quick Reference

| Value | Behavior | Use For |
|-------|----------|---------|
| `aria-live="polite"` | Announced at next pause | Status updates, confirmations |
| `aria-live="assertive"` | Announced immediately | Errors, time-sensitive alerts |
| `role="status"` | Same as polite | Status messages |
| `role="alert"` | Same as assertive | Error messages |

## Testing Tools

```bash
# Automated audit
npx axe-core          # Programmatic accessibility testing
npx pa11y             # CLI accessibility checker

# In browser: Chrome DevTools → Lighthouse → Accessibility
# In browser: Chrome DevTools → Elements → Accessibility tree

# Screen reader testing
# macOS: VoiceOver (Cmd + F5)
# Windows: NVDA (free) or JAWS
# Linux: Orca
```

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `div` as button | Not focusable, no keyboard | Use `<button>` |
| Missing `alt` text | Images invisible to screen readers | Add descriptive `alt` |
| Color-only states | Invisible to color-blind users | Add icons, text, patterns |
| Autoplaying media | Disorienting, can't stop | Add controls, don't autoplay |
| Custom dropdown no ARIA | Unusable by keyboard/screen reader | Native `<select>` or ARIA listbox |
| Removing focus outlines | Can't see focus position | Style outlines, don't remove |
| Empty links/buttons | "Link" with no description | Add text or `aria-label` |
| `tabindex > 0` | Breaks natural tab order | Use `tabindex="0"` or `-1` only |
