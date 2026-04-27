# Flyer / Poster / Brochure Workflow

Create print-ready marketing flyers, posters, handouts, and brochures using Typst.

## When to Use

| Request | Template |
|---------|----------|
| Single-page flyer, handout, leaflet | Single-page scaffold below |
| Front + back flyer (2 pages) | Two-page scaffold below |
| Multi-page brochure | Two-page scaffold extended + `bookletic` for imposition |
| Poster, wall display | Single-page scaffold with larger paper size |

## Print Formats

| Format | Paper | Margins | Bleed | Use Case |
|--------|-------|---------|-------|----------|
| A4 Flyer | `"a4"` | `0cm` | 3mm | Standard European flyer |
| A5 Flyer | `"a5"` | `0cm` | 3mm | Half-page handout |
| Letter | `"us-letter"` | `0cm` | 3.2mm (0.125in) | US standard flyer |
| A3 Poster | `"a3"` | `0cm` | 3mm | Wall poster |
| A2 Poster | Custom `(420mm, 594mm)` | `0cm` | 5mm | Large format |

**Print rules:**
- Use `0cm` margins — flyer layouts use `#place()` for absolute positioning
- Add 3mm bleed for edge-to-edge color (extend backgrounds beyond trim)
- Keep text 10mm+ from edges (safe zone for cutting tolerance)
- High contrast text — print loses ~10% contrast vs screen
- Embed images as local files, not URLs — Typst requires local paths

## Key Typst Patterns for Flyers

### Full-bleed background color
```typst
#place(top + left)[
  #rect(fill: rgb("#3a2e1f"), width: 100%, height: 100%)
]
```

### Image as background (full page)
```typst
#place(top + left)[
  #image("hero.jpg", width: 100%, height: 100%, fit: "cover")
]
```

### Semi-transparent overlay on image
```typst
// Image first
#place(top + left)[
  #image("hero.jpg", width: 100%, height: 100%, fit: "cover")
]
// Dark overlay for text readability
#place(top + left)[
  #rect(fill: rgb("#000000").transparentize(40%), width: 100%, height: 100%)
]
// Text on top
#place(center + horizon)[
  #text(fill: white, size: 48pt, weight: "bold")[Your Headline]
]
```

### Colored section band
```typst
#place(bottom + left, dy: -8cm)[
  #rect(fill: rgb("#f5f0eb"), width: 100%, height: 8cm)[
    #pad(x: 2cm, y: 1cm)[
      #text(size: 12pt)[Section content here]
    ]
  ]
]
```

### Two-column layout within a section
```typst
#place(left + top, dx: 2cm, dy: 15cm)[
  #grid(
    columns: (8cm, 8cm),
    gutter: 1cm,
    [Left column content],
    [Right column content],
  )
]
```

### Rounded image inset
```typst
#place(left + top, dx: 3cm, dy: 12cm)[
  #box(clip: true, radius: 8pt, width: 6cm)[
    #image("photo.jpg", width: 100%, fit: "cover")
  ]
]
```

### QR code (if `@preview/cades` is available)
```typst
#import "@preview/cades:0.3.0": qr-code
#place(right + bottom, dx: -2cm, dy: -2cm)[
  #qr-code("https://yoursite.com", width: 3cm)
]
```

## Single-Page Flyer Scaffold

```typst
#set page(paper: "a4", margin: 0cm)
#set text(font: "Lato", size: 11pt, lang: "de")

// --- Color Palette (customize per brand) ---
#let primary = rgb("#3a2e1f")     // Dark earth brown
#let secondary = rgb("#5f6360")   // Warm gray
#let accent = rgb("#8b6f47")      // Golden brown
#let bg-light = rgb("#f5f0eb")    // Warm cream
#let text-dark = rgb("#2a2a2a")   // Near-black
#let text-light = white

// --- Hero Section (top 50%) ---
#place(top + left)[
  #image("hero.jpg", width: 100%, height: 50%, fit: "cover")
]
#place(top + left)[
  #rect(fill: primary.transparentize(50%), width: 100%, height: 50%)
]
#place(left + top, dx: 2.5cm, dy: 3cm)[
  #text(fill: text-light, size: 14pt, tracking: 0.15em, weight: "regular")[
    YOUR BRAND
  ]
]
#place(left + top, dx: 2.5cm, dy: 5cm)[
  #text(fill: text-light, size: 36pt, weight: "bold")[
    Main Headline
  ]
]
#place(left + top, dx: 2.5cm, dy: 8cm)[
  #text(fill: text-light, size: 14pt)[
    Supporting tagline or short description
  ]
]

// --- Content Section (bottom 50%) ---
#place(bottom + left)[
  #rect(fill: bg-light, width: 100%, height: 50%)[
    #pad(x: 2.5cm, y: 2cm)[
      #text(fill: text-dark, size: 12pt)[
        Body copy goes here. Describe the offering,
        event, or product with compelling language.
      ]

      #v(1cm)

      #text(fill: accent, size: 11pt, weight: "bold")[
        Call to Action or Contact Info
      ]
    ]
  ]
]
```

## Two-Page (Front + Back) Flyer Scaffold

```typst
#set page(paper: "a4", margin: 0cm)
#set text(font: "Lato", size: 11pt, lang: "de")

// --- Color Palette (customize per brand) ---
#let primary = rgb("#3a2e1f")
#let secondary = rgb("#5f6360")
#let accent = rgb("#8b6f47")
#let bg-light = rgb("#f5f0eb")
#let text-dark = rgb("#2a2a2a")
#let text-light = white

// ============================================
// PAGE 1 — FRONT
// ============================================

// Hero image — full bleed
#place(top + left)[
  #image("hero.jpg", width: 100%, height: 60%, fit: "cover")
]
// Gradient overlay
#place(top + left)[
  #rect(fill: primary.transparentize(40%), width: 100%, height: 60%)
]

// Brand name
#place(left + top, dx: 2.5cm, dy: 2cm)[
  #text(fill: text-light, size: 14pt, tracking: 0.15em)[YOUR BRAND]
]

// Main headline
#place(left + top, dx: 2.5cm, dy: 5cm)[
  #text(fill: text-light, size: 42pt, weight: "bold")[
    Headline
  ]
]

// Tagline
#place(left + top, dx: 2.5cm, dy: 9cm)[
  #text(fill: text-light, size: 16pt)[
    Compelling tagline or short description
  ]
]

// Bottom content area
#place(bottom + left)[
  #rect(fill: bg-light, width: 100%, height: 40%)[
    #pad(x: 2.5cm, y: 2cm)[
      #text(fill: text-dark, size: 13pt, weight: "bold")[
        Key Offering Title
      ]
      #v(0.5cm)
      #text(fill: secondary, size: 11pt)[
        Description of what's included, what makes it special,
        and why the reader should care.
      ]
    ]
  ]
]

// ============================================
// PAGE 2 — BACK
// ============================================
#pagebreak()

// Full background color
#place(top + left)[
  #rect(fill: bg-light, width: 100%, height: 100%)
]

// Secondary image
#place(top + left, dx: 2.5cm, dy: 2cm)[
  #box(clip: true, radius: 8pt, width: 15cm, height: 8cm)[
    #image("secondary.jpg", width: 100%, fit: "cover")
  ]
]

// Details section
#place(left + top, dx: 2.5cm, dy: 12cm)[
  #box(width: 15cm)[
    #text(fill: primary, size: 20pt, weight: "bold")[
      More Details
    ]
    #v(0.8cm)
    #text(fill: text-dark, size: 11pt)[
      Additional information, pricing, schedule,
      or whatever belongs on the back of the flyer.
    ]
  ]
]

// Contact footer
#place(bottom + left, dy: 0cm)[
  #rect(fill: primary, width: 100%, height: 5cm)[
    #pad(x: 2.5cm, y: 1.2cm)[
      #text(fill: text-light, size: 12pt, weight: "bold")[
        Contact & Website
      ]
      #v(0.3cm)
      #text(fill: text-light.transparentize(20%), size: 10pt)[
        phone · email · website.com
      ]
    ]
  ]
]
```

## Compile

```bash
typst compile flyer.typ flyer.pdf
```

Open in browser or PDF viewer to verify layout before printing.

## Multi-Page Brochure

For brochures with 4+ pages that need to be printed as a folded booklet:

```typst
#import "@preview/bookletic:0.3.2": sig

// Design your pages normally, then wrap in sig() for imposition
#sig(pages: 8)[
  // Your 8 pages of content here
]
```

This arranges pages in the correct order for double-sided printing and folding.

## Brand Extraction Checklist

When designing a flyer for an existing brand (website, business), extract these assets **before** writing any Typst code. Use a BrowserAgent for JS-rendered sites (Wix, Squarespace, Webflow) — `WebFetch` returns empty content for SPAs.

### 1. Colors (required)
- [ ] Page background color (often off-white, not pure `#fff`)
- [ ] Primary text / dark color
- [ ] Accent color (CTAs, highlights, links)
- [ ] Secondary accent (borders, dividers, subtle elements)
- [ ] Any additional brand colors

**How:** Inspect CSS custom properties (`--color_*` vars) or computed `background-color` / `color` on key elements. Record as hex values.

### 2. Typography (required)
- [ ] Heading font family
- [ ] Body font family
- [ ] Check if fonts are available locally: `typst fonts | grep -i "fontname"`
- [ ] Pick fallbacks from PAI verified fonts if not installed (Lato, Ubuntu Sans, Libertinus Serif)

### 3. Images (required)
- [ ] Hero / banner images — download full resolution
- [ ] Product / service photos
- [ ] Team / portrait photos
- [ ] Logo (SVG preferred, PNG fallback)
- [ ] Verify all downloads are real images: `file *.jpg *.png`

**How:** Extract `src` URLs from `<img>` tags or CSS `background-image`. For Wix: look for `static.wixstatic.com/media/` URLs. Download via `curl -sL -o name.jpg "URL"`.

### 4. Copy / Text (required)
- [ ] Business name and tagline
- [ ] Service/product descriptions (use verbatim — client wrote it for a reason)
- [ ] Pricing, hours, availability details
- [ ] Contact: phone, email, address, WhatsApp, social media
- [ ] Website URL for QR code

### 5. Brand Personality (inform design choices)
- [ ] Formal vs casual tone?
- [ ] Luxury vs rustic vs modern vs playful?
- [ ] Target audience?

### Output
Map extracted assets to Typst variables:
```typst
// Brand palette
#let primary = rgb("#...")
#let accent = rgb("#...")
#let bg = rgb("#...")

// Brand fonts (or closest PAI fallback)
#set text(font: "...", lang: "...")
```

## Typst Gotchas for Flyers

- **`gradient.linear` + `transparentize()` doesn't work visually over images** — use stacked semi-transparent `#rect` layers instead
- **Image paths are relative to the `.typ` file** — keep images in the same directory
- **`height: 50%` on images inside `#place()`** may not resolve to page height — use absolute dimensions (`height: 14.8cm`)
- **`fit: "cover"` requires a constrained container** — wrap in `#box(width: X, height: Y, clip: true)`

## Tips

- **Start with `#place()`** — flyer design is absolute positioning, not document flow
- **Layer order matters** — Typst draws in source order. Background first, then overlays, then text
- **Test print at home first** — colors and text sizing always look different on paper
- **Safe zone**: keep important text 10mm from all edges
- **Font pairing**: one display/heading font + one body font maximum
- **Less is more**: flyers need whitespace. Don't fill every cm²
