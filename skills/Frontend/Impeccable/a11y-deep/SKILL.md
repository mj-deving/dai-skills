---
name: a11y-deep
description: Deep WCAG 2.2 AA accessibility audit using specialist agents. Use for public-facing pages, portfolio deploys, or when Impeccable/audit flags a11y issues. Slower than /audit but catches everything.
version: 1.0.0
user-invocable: true
argument-hint: "[file or URL to audit]"
---

# Deep Accessibility Audit

Full WCAG 2.2 AA compliance review using specialist agents from the `accessibility-agents` plugin. This is the **deep dive** — use it before shipping public-facing work.

## When to Use

| Situation | Use `/audit` (quick) | Use `/a11y-deep` (this) |
|---|---|---|
| Every build | Yes | No |
| Before deploying portfolio | Yes first, then | Yes |
| Complex forms or modals | Maybe enough | Yes |
| Impeccable/audit flags a11y score < 3 | Already ran | Yes — dig deeper |
| Client/public-facing work | Yes first, then | Yes |
| Internal dashboards | Yes | No — overkill |

## Workflow

### Step 1: Identify the target

Read the file(s) to audit. Accept:
- A single HTML file path
- A component directory
- A URL (if Playwright MCP is available for live audit)

### Step 2: Run specialist agents (parallel where possible)

The `accessibility-agents` plugin lives at:
`${AGENT_HOME}/plugins/cache/community-access/accessibility-agents/3.2.0/agents/`

Load the relevant specialist prompt files and apply their checklists to the target code. Run these checks **yourself** using the specialist's checklist — do NOT try to spawn them as subagents (the subagent_type is not registered).

**Core specialists to consult (always):**

| Specialist | File | Checks |
|---|---|---|
| Contrast Master | `contrast-master.md` | Color contrast ratios, focus indicators, dark mode, `prefers-*` media queries |
| ARIA Specialist | `aria-specialist.md` | Roles, states, properties, widget patterns, landmark structure |
| Keyboard Navigator | `keyboard-navigator.md` | Tab order, focus management, skip links, keyboard traps |
| Alt Text & Headings | `alt-text-headings.md` | Image descriptions, heading hierarchy, landmark labels |
| Link Checker | `link-checker.md` | Ambiguous link text ("click here", "learn more"), new-tab warnings |

**Conditional specialists (invoke when relevant):**

| Specialist | File | When |
|---|---|---|
| Forms Specialist | `forms-specialist.md` | Page has `<form>`, `<input>`, `<select>`, `<textarea>` |
| Modal Specialist | `modal-specialist.md` | Page has modals, dialogs, drawers, popovers |
| Tables Data Specialist | `tables-data-specialist.md` | Page has `<table>` elements |
| Live Region Controller | `live-region-controller.md` | Page has dynamic content updates, toasts, notifications |
| Design System Auditor | `design-system-auditor.md` | Auditing a component library or design system |

### Step 3: Compile findings

Format as severity-rated report:

```markdown
## Deep Accessibility Audit: [filename]

### Summary
- **WCAG Level:** [A / AA / Partial AA / Fails AA]
- **Critical Issues:** [count]
- **Major Issues:** [count]
- **Minor Issues:** [count]

### Critical (must fix before ship)
1. [WCAG criterion] — [issue] — [fix]

### Major (should fix)
1. [WCAG criterion] — [issue] — [fix]

### Minor (nice to fix)
1. [WCAG criterion] — [issue] — [fix]

### Passing
- [List what passes — gives confidence, not just problems]
```

### Step 4: Fix or report

- If invoked with "fix" in the request: apply fixes directly
- If invoked as audit only: report findings, let user decide

## What This Does NOT Cover

These specialists are NOT included (out of scope for web frontend):
- PDF/Word/Excel/PowerPoint accessibility (use document-accessibility-wizard if needed)
- Desktop app accessibility (NVDA, JAWS — irrelevant for web)
- GitHub DevOps (25 agents for repo management — not a11y)
- Mobile native (React Native, SwiftUI — separate concern)

## Integration with Impeccable Pipeline

```
Quick gate:    /audit           → 5-dimension scored report (run every time)
Deep dive:     /a11y-deep       → full WCAG specialist review (run before deploy)
Production:    /harden          → cross-browser, edge cases, performance
```

The recommended flow in BrandedBuild Step 4 is: `/audit` first. If a11y score < 3, escalate to `/a11y-deep`.
