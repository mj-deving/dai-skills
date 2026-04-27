# Cover Letter / Application Letter Workflow

Generate a professional cover letter or application letter as PDF.

## Step 1: Gather Information

Check if the user has provided letter context. If not, ask for:
- **Recipient:** Company name, hiring manager (if known), address
- **Position:** Job title being applied for
- **Source:** Where the job was found (optional, for opening line)
- **Key qualifications:** 2-3 strongest matches between their background and the job requirements
- **Motivation:** Why this company specifically (not generic)

Also check:
- `${PAI_USER_DIR}/TELOS/` for career context
- Any CV recently generated in this session (reuse contact info, experience)

## Step 2: Choose Letter Style

| Style | When to Use |
|-------|------------|
| **Professional** (default) | Standard business letter, formal but warm |
| **Academic** | University positions, research roles, includes research interests |
| **Creative** | Design/marketing/startup roles, more personality |
| **German formal** | German-language applications, DIN 5008 compliant |

## Step 3: Generate Typst Source

### PAI Professional Letter Template

```typst
// Professional Cover Letter
#set page(paper: "a4", margin: (top: 2.5cm, bottom: 2cm, left: 2.5cm, right: 2.5cm))
#set text(font: "Libertinus Serif", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.7em, first-line-indent: 0em)

#let accent = rgb("#1e3a5f")
#let subtle = rgb("#6b7280")

// Sender info (top right)
#align(right)[
  #text(weight: "bold", size: 12pt)[Full Name] \
  #text(subtle, size: 10pt)[
    Street Address \
    City, Postal Code \
    email\@example.com \
    +49 123 456 7890
  ]
]

#v(1.5cm)

// Date
#text(subtle, size: 10pt)[#datetime.today().display("[month repr:long] [day], [year]")]

#v(0.8cm)

// Recipient
Company Name \
Hiring Manager Name \
Street Address \
City, Postal Code

#v(1cm)

// Subject line
#text(weight: "bold", size: 11.5pt)[Re: Application for Position Title]

#v(0.8cm)

// Salutation
Dear Hiring Manager,

#v(0.4cm)

// Opening paragraph — hook + why this company
Opening paragraph that immediately connects your strongest qualification to the company's specific need. Reference why THIS company, not any company. 1-2 sentences max.

// Body paragraph 1 — strongest qualification match
Your most relevant experience or achievement, directly mapped to a key requirement from the job posting. Use specific numbers and outcomes.

// Body paragraph 2 — second match + cultural fit
A complementary qualification that shows breadth. Connect to company values, culture, or mission if genuine.

// Closing paragraph — call to action
Express enthusiasm for discussing further. Reference availability. Thank for consideration.

#v(0.5cm)

Sincerely,

#v(1.2cm)

Full Name
```

### German DIN 5008 Variant

For German applications, adjust:
- Date format: `TT.MM.JJJJ`
- Salutation: `Sehr geehrte Damen und Herren,` or `Sehr geehrte/r Frau/Herr [Name],`
- Closing: `Mit freundlichen Grüßen`
- Address block on the left
- Subject line bold, no "Re:"
- Language: `#set text(lang: "de")`

## Step 4: Writing Guidelines

**DO:**
- Open with something specific about the company (recent project, mission, product)
- Map each qualification directly to a job requirement
- Use active verbs and specific numbers ("increased by 40%", "led a team of 8")
- Keep to one page — no exceptions
- Match the tone of the company (startup vs corporate)

**DON'T:**
- Start with "I am writing to apply for..." (boring, wastes the opening)
- Repeat the CV verbatim — the letter adds context and narrative
- Use generic praise ("your prestigious company")
- Include salary expectations unless explicitly asked

## Step 5: Compile and Verify

```bash
typst compile letter.typ letter.pdf
```

Verify:
- [ ] Fits on exactly one page
- [ ] Sender and recipient info are complete
- [ ] Date is correct
- [ ] No placeholder text remains
- [ ] Consistent with CV styling (if both were generated)

## Step 6: Offer Matching Set

- "Want me to generate a matching CV in the same style?"
- "Should I create a German version too?"
- "Want a shorter email version of this letter?"
