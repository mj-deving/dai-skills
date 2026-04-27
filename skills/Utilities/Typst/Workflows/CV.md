# CV / Resume Workflow

Generate a professional, ATS-friendly CV as PDF.

## Step 1: Gather Information

Check if the user has provided CV data. If not, check these sources:
1. `${PAI_USER_DIR}/TELOS/GOALS.md` — career goals, current role
2. `${PAI_USER_DIR}/TELOS/PROJECTS.md` — project history
3. Ask the user for missing essentials:
   - Full name, contact info, location
   - Professional summary / tagline
   - Work experience (company, role, dates, achievements)
   - Education
   - Skills
   - Languages (if relevant)

## Step 2: Choose Template Style

Ask the user (or use default based on context):

| Style | When to Use | Layout |
|-------|------------|--------|
| **Modern** (default) | Tech, startups, creative | Two-column, accent color sidebar, sans-serif |
| **Classic** | Traditional industries, academia | Single-column, serif, understated |
| **Minimal** | Design roles, when content speaks | Maximum whitespace, thin rules, no color |
| **ATS-optimized** | Online applications, keyword parsing | Single-column, no columns/graphics, plain structure |

If the user has a specific Typst Universe template in mind, use `typst init @preview/{template}` instead.

## Step 3: Generate Typst Source

Write a `.typ` file using the PAI CV template structure below. Adapt sections to the user's data.

### PAI Modern CV Template

```typst
// Modern CV — two-column with accent sidebar
#set page(paper: "a4", margin: (top: 1.5cm, bottom: 1.5cm, left: 1.5cm, right: 1.5cm))
#set text(font: "Ubuntu Sans", size: 10pt)
#set par(leading: 0.6em)

#let accent = rgb("#1e3a5f")
#let light-bg = rgb("#f0f4f8")
#let subtle = rgb("#6b7280")

#let section(title) = {
  v(0.8em)
  text(accent, weight: "bold", size: 12pt, upper(title))
  v(0.3em)
  line(length: 100%, stroke: 0.5pt + accent)
  v(0.4em)
}

#let entry(title, subtitle, dates, body) = {
  grid(
    columns: (1fr, auto),
    text(weight: "bold", title),
    text(subtle, size: 9pt, dates),
  )
  if subtitle != none {
    text(subtle, size: 9.5pt, subtitle)
  }
  v(0.2em)
  body
  v(0.5em)
}

// Header
#align(center)[
  #text(size: 24pt, weight: "bold", [FULL NAME])
  #v(0.3em)
  #text(subtle, size: 10pt)[
    email\@example.com | +49 123 456 7890 | City, Country |
    #link("https://linkedin.com/in/handle")[LinkedIn] |
    #link("https://github.com/handle")[GitHub]
  ]
]

#v(0.5em)
#line(length: 100%, stroke: 1pt + accent)
#v(0.3em)

// Professional Summary
#text(style: "italic", size: 10.5pt)[
  Brief 2-3 sentence summary of professional identity and key strengths.
]

#v(0.3em)

// Experience
#section("Experience")
#entry(
  "Job Title",
  "Company Name",
  "Jan 2023 — Present",
  [
    - Achievement with measurable impact
    - Another achievement with specific numbers
    - Technology or methodology highlight
  ]
)

// Education
#section("Education")
#entry(
  "Degree Name",
  "University Name",
  "2018 — 2022",
  []
)

// Skills
#section("Skills")
#grid(
  columns: (1fr, 1fr),
  gutter: 0.5em,
  [*Languages:* Skill 1, Skill 2, Skill 3],
  [*Frameworks:* Framework 1, Framework 2],
  [*Tools:* Tool 1, Tool 2, Tool 3],
  [*Languages:* English (native), German (B2)],
)
```

**Adapt this template:** Replace placeholder content with the user's actual data. Add/remove sections as needed (certifications, publications, volunteer work, etc.).

## Step 4: Compile and Verify

```bash
typst compile cv.typ cv.pdf
```

Open the PDF and verify:
- [ ] All text is readable, no overflow
- [ ] Dates align properly
- [ ] Fits on 1-2 pages (never more for a CV)
- [ ] No orphaned section headers at page bottom
- [ ] Contact info is complete and correct

## Step 5: Offer Variations

After the first version:
- "Want me to adjust the style? (more compact, different color, single-column)"
- "Should I create an ATS-optimized version too?"
- "Want a matching cover letter?"
