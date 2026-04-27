---
name: Component Patterns
description: Component architecture, anti-AI-slop design rules, state management, and design system adherence with code examples
source: addyosmani/agent-skills frontend-ui-engineering (MIT), Anthropic frontend-design (Apache 2.0)
---

# Component Patterns & Anti-AI-Slop Rules

## Design Thinking (from Anthropic)

Before coding, understand context and commit to a **BOLD aesthetic direction**:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick a clear direction — brutally minimal, maximalist, retro-futuristic, organic/natural, luxury/refined, playful, editorial/magazine, brutalist/raw, art deco, industrial/utilitarian
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

## Anti-AI-Slop Table

AI-generated UI has recognizable patterns. Avoid all of them:

| AI Default | Why It's a Problem | Production Quality |
|---|---|---|
| Purple/indigo everything | Models default to "safe" palettes, every app looks identical | Use the project's actual color palette |
| Excessive gradients | Gradients add noise and clash with most design systems | Flat or subtle gradients matching the design system |
| Rounded everything (rounded-2xl) | Maximum rounding ignores hierarchy of corner radii in real designs | Consistent border-radius from the design system |
| Generic hero sections | Template layout with no connection to actual content | Content-first layouts |
| Lorem ipsum-style copy | Placeholder hides layout problems real content reveals | Realistic placeholder content |
| Oversized padding everywhere | Equal generous padding destroys visual hierarchy, wastes space | Consistent spacing scale |
| Stock card grids | Uniform grids ignore information priority and scanning patterns | Purpose-driven layouts |
| Shadow-heavy design | Layered shadows compete with content, slow rendering | Subtle or no shadows unless design system specifies |
| Generic fonts (Inter, Roboto, Arial) | Lack character, signal "default AI output" | Distinctive, context-appropriate font choices |
| Cliched color schemes | Particularly purple gradients on white backgrounds | Dominant colors with sharp accents |

**NEVER converge on common AI choices across generations.** Vary between light/dark themes, different fonts, different aesthetics. Each design should feel genuinely crafted for its context.

## Aesthetics Guidelines (from Anthropic)

- **Typography**: Choose distinctive, characterful fonts. Pair a display font with a refined body font. Avoid Inter, Roboto, Arial, system fonts.
- **Color & Theme**: CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Focus on high-impact moments — one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds**: Atmosphere and depth, not solid colors. Gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, grain overlays.

## Component Architecture

### File Structure — Colocate Everything

```
src/components/
  TaskList/
    TaskList.tsx          # Component
    TaskList.test.tsx     # Tests
    TaskList.stories.tsx  # Storybook (if using)
    use-task-list.ts      # Custom hook (if complex state)
    types.ts              # Component-specific types
```

### Composition Over Configuration

```tsx
// Good: Composable
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// Avoid: Over-configured
<Card title="Tasks" headerVariant="large" bodyPadding="md"
  content={<TaskList tasks={tasks} />} />
```

### Separate Data Fetching from Presentation

```tsx
// Container: handles data
export function TaskListContainer() {
  const { tasks, isLoading, error } = useTasks();
  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="Failed to load tasks" retry={refetch} />;
  if (tasks.length === 0) return <EmptyState message="No tasks yet" />;
  return <TaskList tasks={tasks} />;
}

// Presentation: handles rendering
export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul role="list" className="divide-y">
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
    </ul>
  );
}
```

## State Management

Choose the simplest approach that works:

```
Local state (useState)           → Component-specific UI state
Lifted state                     → Shared between 2-3 siblings
Context                          → Theme, auth, locale (read-heavy, write-rare)
URL state (searchParams)         → Filters, pagination, shareable UI state
Server state (React Query, SWR)  → Remote data with caching
Global store (Zustand, Redux)    → Complex client state shared app-wide
```

**Avoid prop drilling deeper than 3 levels.** If passing props through components that don't use them, introduce context or restructure.

## Spacing and Layout

Use a consistent spacing scale. Don't invent values:

```css
/* Use the scale: 0.25rem increments (or project's scale) */
/* Good */  padding: 1rem;      /* 16px */
/* Good */  gap: 0.75rem;       /* 12px */
/* Bad */   padding: 13px;      /* Not on any scale */
/* Bad */   margin-top: 2.3rem; /* Not on any scale */
```

## Typography Hierarchy

```
h1 → Page title (one per page)
h2 → Section title
h3 → Subsection title
body → Default text
small → Secondary/helper text
```

Don't skip heading levels. Don't use heading styles for non-heading content.

## Color

- Use semantic color tokens: `text-primary`, `bg-surface`, `border-default` — not raw hex
- Ensure contrast (4.5:1 normal text, 3:1 large text)
- Color is never the sole information carrier

## Loading and Transitions

```tsx
// Skeleton loading (not spinners for content areas)
function TaskListSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading tasks">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-12 bg-muted animate-pulse rounded" />
      ))}
    </div>
  );
}
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Accessibility is a nice-to-have" | Legal requirement in many jurisdictions and an engineering quality standard |
| "We'll make it responsive later" | Retrofitting responsive is 3x harder than building it from the start |
| "The design isn't final, so I'll skip styling" | Use design system defaults. Unstyled UI creates broken first impression |
| "This is just a prototype" | Prototypes become production code. Build the foundation right |
| "The AI aesthetic is fine for now" | It signals low quality. Use the project's actual design system from the start |
