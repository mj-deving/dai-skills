---
name: brand-references
description: 76 brand design systems as DESIGN.md references — 7 bundled locally (Apple, Claude, Cursor, Figma, Spotify, Stripe, Vercel), 69+ fetchable on demand from getdesign.md. Use as starting point for design inspiration, then customize. USE WHEN brand design, design like stripe, design like apple, design inspiration, brand reference, design system reference, getdesign, design.md, start from brand, copy brand style, look like vercel, build like spotify, design reference.
---

# Brand Design References

76 real brand design systems in Google Stitch DESIGN.md format. Use as inspiration and starting point, then customize to make it yours.

## Three Modes

### 1. Browse Bundled Brands (Instant)

7 design systems cached locally — no network needed:

| Brand | Archetype | File |
|-------|-----------|------|
| **Apple** | Extreme restraint, SF Pro, white space | `apple.md` |
| **Claude** | Warm editorial, parchment tones, approachable | `claude.md` |
| **Cursor** | AI-native complex, dark mode, code-first | `cursor.md` |
| **Figma** | Precision tooling, clean grids, bright accents | `figma.md` |
| **Spotify** | Dark content-first, green accent, bold type | `spotify.md` |
| **Stripe** | Premium fintech, purple gradients, weight-300 | `stripe.md` |
| **Vercel** | Cold monochrome, Geist font, minimal | `vercel.md` |

**To use:** Read the relevant `.md` file from this directory, then tell Claude Code:

```
Use this DESIGN.md as the foundation for my site.
Customize it: change the accent color to [HEX], swap the font to [FONT],
and adjust the tone to feel more [DESCRIPTION].
```

### 2. Fetch Any Brand On Demand (69+ more)

For brands not bundled locally, fetch from getdesign.md:

```bash
cd /tmp && npx getdesign@latest add <brand-name>
```

**Available brands include:** Airbnb, Airtable, Binance, BMW, Bugatti, Cal, ClickHouse, Cohere, Coinbase, Composio, ElevenLabs, Expo, Ferrari, Framer, HashiCorp, IBM, Intercom, Kraken, Lamborghini, Linear, Lovable, Mastercard, Meta, Mintlify, Miro, Mistral, MongoDB, Nike, Notion, NVIDIA, Ollama, Pinterest, PlayStation, PostHog, Raycast, Renault, Resend, Revolut, Sanity, Sentry, Shopify, SpaceX, Supabase, Superhuman, Tesla, The Verge, Together.ai, Uber, Vodafone, Warp, Webflow, WIRED, Wise, X.ai, Zapier

After fetching, copy to this directory if you want to keep it:
```bash
cp ${TMPDIR}/DESIGN.md ${SKILLS_HOME}/Frontend/Aesthetics/brand-references/<brand>.md
```

### 3. Generate Custom from Scratch

When no existing brand matches your vision, use the **stitch-skill** to generate a DESIGN.md from scratch:

```
Generate a DESIGN.md for my project.
Mood: [DESCRIPTION]
Industry: [TYPE]
Color direction: [DARK/LIGHT/SPECIFIC]
```

This invokes `Aesthetics/stitch-skill/SKILL.md` which generates a full 9-section DESIGN.md using anti-slop rules.

## Recommended Workflow

1. **Browse** the 7 bundled brands — read 2-3 that feel closest to your vision
2. **Pick one** as your starting foundation
3. **Customize** — don't use it as-is, make it yours:
   - Change the accent color
   - Swap the font family (respect the anti-slop font bans)
   - Adjust the atmosphere description to match your brand
   - Remove sections that don't apply (e.g., fintech shadows for a blog)
   - Add sections specific to your project
4. **Save as DESIGN.md** in your project root — Claude Code reads it automatically

## What Each DESIGN.md Contains

Every file follows the Google Stitch 9-section standard:

1. **Visual Theme & Atmosphere** — mood, density, and design philosophy
2. **Color Palette & Roles** — every hex code with semantic name and usage
3. **Typography Rules** — font families, size hierarchy, weights, spacing
4. **Component Stylings** — buttons, cards, inputs with interaction states
5. **Layout Principles** — grid systems, spacing, whitespace philosophy
6. **Depth & Elevation** — shadows, surface hierarchy, layering
7. **Do's and Don'ts** — design guardrails specific to that brand
8. **Responsive Behavior** — breakpoints, mobile collapse rules
9. **Agent Prompt Guide** — quick reference for LLM-based generation

Files range from 12KB-20KB with 220-320 lines of detailed specifications.

## Integration with Other Skills

- **stitch-skill** — generates new DESIGN.md files from scratch
- **WebsiteFactory** — reads DESIGN.md during PremiumSite workflow
- **FrontendDesign** — anti-slop rules complement brand references
- **UIUXProMax** — data-driven palette/font search when customizing

## Anti-Patterns

- **Don't use brand references unmodified.** You'll get a Stripe clone, not your site. Always customize.
- **Don't mix two brand references.** Pick one foundation. Cherry-picking colors from Stripe and typography from Apple creates visual chaos.
- **Don't use brands that conflict with your content.** Spotify's dark theme works for media; it's wrong for a medical site.
