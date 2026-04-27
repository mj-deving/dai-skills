---
name: Accessibility Guidelines
description: WCAG 2.1 AA implementation guide with code examples — keyboard nav, ARIA, focus management, screen readers, forms
source: addyosmani/agent-skills frontend-ui-engineering (MIT), Anthropic frontend-design
---

# Accessibility Guidelines (WCAG 2.1 AA)

For the quick checklist, see `${SKILLS_HOME}/Utilities/References/accessibility-checklist.md`.
This file provides **implementation patterns with code examples**.

## Keyboard Navigation

Every interactive element must be keyboard accessible:

```tsx
// ✓ Focusable by default
<button onClick={handleClick}>Click me</button>

// ✗ Not focusable — screen readers and keyboard users can't reach it
<div onClick={handleClick}>Click me</div>

// ✓ Works but prefer <button>
<div role="button" tabIndex={0} onClick={handleClick}
     onKeyDown={e => e.key === 'Enter' && handleClick()}>
  Click me
</div>
```

## ARIA Labels

```tsx
// Label interactive elements that lack visible text
<button aria-label="Close dialog"><XIcon /></button>

// Label form inputs
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Or use aria-label when no visible label exists
<input aria-label="Search tasks" type="search" />
```

## Focus Management

```tsx
// Move focus when content changes
function Dialog({ isOpen, onClose }: DialogProps) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) closeRef.current?.focus();
  }, [isOpen]);

  return (
    <dialog open={isOpen}>
      <button ref={closeRef} onClick={onClose}>Close</button>
      {/* Trap focus inside dialog when open */}
    </dialog>
  );
}
```

## Meaningful Empty and Error States

```tsx
// Don't show blank screens
function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) {
    return (
      <div role="status" className="text-center py-12">
        <TasksEmptyIcon className="mx-auto h-12 w-12 text-muted" />
        <h3 className="mt-2 text-sm font-medium">No tasks</h3>
        <p className="mt-1 text-sm text-muted">Get started by creating a new task.</p>
        <Button className="mt-4" onClick={onCreateTask}>Create Task</Button>
      </div>
    );
  }
  return <ul role="list">...</ul>;
}
```

## ARIA Live Regions

| Value | Behavior | Use For |
|-------|----------|---------|
| `aria-live="polite"` | Announced at next pause | Status updates, confirmations |
| `aria-live="assertive"` | Announced immediately | Errors, time-sensitive alerts |
| `role="status"` | Same as polite | Status messages |
| `role="alert"` | Same as assertive | Error messages |

## Design-Level Accessibility

### Color & Contrast
- Text contrast >= 4.5:1 (normal) or >= 3:1 (large text, 18px+)
- UI component contrast >= 3:1 against background
- **Never use color as the sole information carrier** — add icons, patterns, text labels
- Test with color blindness simulators (protanopia, deuteranopia, tritanopia)

### Typography
- Base font size >= 16px (prevents iOS zoom on input focus)
- Line height >= 1.5 for body text
- Max line length ~65-75 characters for readability
- Don't disable text resizing (`user-scalable=no` is an anti-pattern)

### Interactive Elements
- Touch targets >= 44x44px on mobile (WCAG 2.5.8)
- Visible focus indicators (never `outline: none` without replacement)
- Disabled states: reduce opacity to 0.5 AND add `aria-disabled`
- Loading states: use `aria-busy="true"` + skeleton or spinner

### Forms
- Every input needs a visible `<label>` (not just placeholder)
- Group related inputs with `<fieldset>` + `<legend>`
- Error messages: specific, associated with field via `aria-describedby`
- Required fields: indicate with text ("Required"), not just asterisk

### Navigation
- Skip-to-content link as first focusable element
- Consistent navigation across pages
- Landmark regions: `<nav>`, `<main>`, `<aside>`, `<footer>`
- Current page indicated in nav (`aria-current="page"`)

### Dynamic Content
- SPA route changes: manage focus to heading or main content
- Modals: trap focus, return focus on close, use `<dialog>` element
- Tooltips: accessible via hover AND focus, dismissable with Escape
- Infinite scroll: provide "Load more" button alternative

## Testing Workflow

1. **Automated:** `npx axe-core` or `npx pa11y` on every page
2. **Keyboard:** Tab through entire UI — can you reach and operate everything?
3. **Screen reader:** Test critical flows with VoiceOver (macOS), NVDA (Windows), Orca (Linux)
4. **Zoom:** Test at 200% zoom — does layout still work?
5. **Color:** Test with color blindness simulator
