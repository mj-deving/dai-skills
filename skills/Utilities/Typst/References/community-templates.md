# Typst Community Templates — Verified Reference

Tested on Typst 0.13.1 (2026-04-14). Only templates that compile clean are listed.

## How to Use

```bash
typst init @preview/{template-name} my-document
cd my-document
# Edit the .typ file(s) with your content
typst compile main.typ output.pdf
```

---

## CV / Resume (9 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/modern-cv` | Two-column, photo, accent color, cover letter included | Best all-rounder — CV + cover letter in one template |
| `@preview/imprecv` | Clean ATS-friendly, single-column, sections with rules | Best for online applications, excellent typography |
| `@preview/basic-resume` | Simple standard resume, ATS-optimized | Minimal, professional, no frills |
| `@preview/acorn-resume` | Clean minimal with flexible sections | Good customizability |
| `@preview/ats-friendly-resume` | Developer-focused ATS resume | Optimized for keyword parsing |
| `@preview/vercanard` | Modern European style | Clean, distinctive |
| `@preview/academicv` | Academic CV from YAML data | Good for long academic CVs, data-driven |
| `@preview/acadennial-cv` | Lifelong academic CV | Comprehensive sections for publications, grants |
| `@preview/bone-resume` | Colorful, Chinese-friendly | Good for creative roles |

### Top Picks
- **General use:** `modern-cv` (includes matching cover letter)
- **ATS/online applications:** `imprecv` or `basic-resume`
- **Academic:** `academicv` (YAML-driven, extensible)

---

## Letters (5 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/appreciated-letter` | Business letter with clean layout | Good for formal correspondence |
| `@preview/briefs` | Simple letter template | Minimal, quick |
| `@preview/aspirationally` | Academic cover letter / teaching statement | Clean, minimal, academic-focused |
| `@preview/letterloom` | Professional with customization | Streamlined professional letters |
| `@preview/formalettre` | French formal letter | DIN-style French correspondence |

### Top Picks
- **Job applications:** `modern-cv` (has built-in cover letter) or PAI Letter workflow
- **Business correspondence:** `appreciated-letter`
- **Academic:** `aspirationally`

---

## Reports (6 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/biz-report` | Multi-chapter business report, cover page, TOC, infoboxes, author cutout | **Best report template** — production-quality |
| `@preview/bubble` | Colorful, modern, clean | Good for lighter reports |
| `@preview/basic-report` | Simple clean report | Quick starting point |
| `@preview/ailab-isetbz` | Lab report for engineering | Structured lab format |
| `@preview/bei-report` | Internship report | Good for work placement reports |
| `@preview/guido` | Beautiful general document | Needs Nunito font |

### Top Pick
- **Business/consulting:** `biz-report` — has everything (cover, TOC, infoboxes, tables, back page)

---

## Invoices (4 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/invoice-pro` | DIN 5008, auto-calculations, EPC QR code | **Best for EU/German invoices** |
| `@preview/invoice-maker` | Beautiful general-purpose invoice | Data-record driven, flexible |
| `@preview/german-fx-invoice` | German freelancer, FX support | International currency support |
| `@preview/inboisu` | Japanese invoice format | Specific to Japanese standards |

### Top Picks
- **German/EU:** `invoice-pro` (DIN 5008, SEPA QR)
- **International:** `invoice-maker`

---

## Academic Papers (6 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/charged-ieee` | IEEE conference format | Most common CS/engineering format |
| `@preview/clean-math-paper` | Clean mathematical paper | Excellent math typesetting |
| `@preview/academic-alt` | Flexible university assignments | Labs, homework, assignments |
| `@preview/adaptable-pset` | Problem set template | Perfect for technical courses |
| `@preview/academic-conf-pre` | Academic presentation slides | Conference presentation format |
| `@preview/axiomst` | Homework + presentation slides | Combined academic template |

### Top Pick
- **Conference papers:** `charged-ieee`
- **Math/science:** `clean-math-paper`

---

## Presentations (4 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/calmly-touying` | Calm, modern Moloch-inspired design | **Best looking presentation** |
| `@preview/basic-polylux` | Starter Polylux template | Needs math font |
| `@preview/slydst` | Simple slides in Typst | Lightweight, no framework needed |
| `@preview/diatypst` | Clean presentation | Simple and effective |

### Frameworks
- **Touying** — the most popular Typst presentation framework (many themes)
- **Polylux** — alternative presentation framework

### Top Pick
- **General:** `calmly-touying` or `slydst`

---

## Thesis (4 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/aio-studi-and-thesis` | All-in-one student/thesis template | Versatile German university format |
| `@preview/athena-tu-darmstadt-thesis` | TU Darmstadt thesis | Specific university branding |
| `@preview/benplate` | Flexible thesis/term paper | Customizable for many universities |
| `@preview/canonical-nthu-thesis` | NTHU dissertations | Needs Chinese fonts |

---

## Posters (4 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/placard` | Modular grid scientific poster | Flexible layout system |
| `@preview/pollux` | Clean minimal academic poster | Gemini-inspired design |
| `@preview/simple-research-poster` | Basic research poster | Quick starting point |
| `@preview/poster-syndrome` | Custom frame placement | Creative poster layouts |

---

## Books (1 verified)

| Template | Style | Notes |
|----------|-------|-------|
| `@preview/bookly` | Book template | Chapter-based, appendices |

---

## Compatibility Notes

- **Typst 0.13.1:** 35 of 41 tested templates compile successfully
- **Typst 0.14.0 required:** `brilliant-cv`, `barcala`, `classy-german-invoice`, `ilm` (upgrade Typst when 0.14 is stable)
- **Font dependencies:** `guido` (Nunito), `canonical-nthu-thesis` (Chinese fonts), `basic-polylux` (Lete Sans Math)
- **Not templates:** `chic-hdr`, `abyss-book`, `bookletic` (these are library packages, not scaffoldable templates)

## Browsing More

```bash
# List all available templates
typst init --list 2>&1 | head -50

# Search Typst Universe online
# https://packages.typst.org
```

Typst Universe has 1,200+ packages total. This reference covers the top 35 that work on our version.
