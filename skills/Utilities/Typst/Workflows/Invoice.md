# Invoice Workflow

Generate professional invoices as PDF.

## Community Templates

```bash
# Professional DIN 5008 invoice with auto-calculations and EPC QR code
typst init @preview/invoice-pro invoice

# Beautiful general-purpose invoice from data records
typst init @preview/invoice-maker invoice

# German freelancer invoice with FX support
typst init @preview/german-fx-invoice invoice

# Japanese invoice format
typst init @preview/inboisu invoice
```

**Recommended:** `@preview/invoice-pro` for German/EU invoices (DIN 5008, EPC QR code, auto-calculations). `@preview/invoice-maker` for international/generic invoices.

## Structure

```
Your company/name + address
Client name + address
Invoice number + date
Due date
Line items table (description, quantity, unit price, total)
Subtotal
Tax (VAT/USt)
Total
Payment details (IBAN, BIC, reference)
Optional: QR code for SEPA payment
```

## PAI Fallback Template

```typst
#set page(paper: "a4", margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm))
#set text(font: "Ubuntu Sans", size: 10pt)

#let accent = rgb("#1e3a5f")

// Header
#grid(
  columns: (1fr, 1fr),
  align(left)[
    #text(weight: "bold", size: 14pt)[Your Name] \
    #text(size: 9pt)[Street \ City, Postal Code \ Tax ID: DE123456789]
  ],
  align(right)[
    #text(accent, weight: "bold", size: 20pt)[INVOICE] \
    #text(size: 10pt)[
      Invoice \#: 2026-001 \
      Date: #datetime.today().display("[day].[month].[year]") \
      Due: 30 days
    ]
  ],
)

#v(1cm)

// Client
*Bill To:* \
Client Name \
Client Address

#v(1cm)

// Line items
#table(
  columns: (3fr, 1fr, 1fr, 1fr),
  stroke: none,
  fill: (_, y) => if y == 0 { accent.lighten(90%) },
  [*Description*], [*Qty*], [*Unit Price*], [*Total*],
  table.hline(stroke: 0.5pt),
  [Consulting services — April 2026], [40h], [EUR 150], [EUR 6,000],
  [Development — API integration], [20h], [EUR 120], [EUR 2,400],
  table.hline(stroke: 0.5pt),
  [], [], [*Subtotal*], [*EUR 8,400*],
  [], [], [VAT 19%], [EUR 1,596],
  table.hline(stroke: 1pt),
  [], [], [*Total*], [*EUR 9,996*],
)

#v(2cm)

// Payment
*Payment Details:* \
IBAN: DE89 3704 0044 0532 0130 00 \
BIC: COBADEFFXXX \
Reference: INV-2026-001
```

## Compile
```bash
typst compile invoice/main.typ invoice.pdf
# or for PAI template:
typst compile invoice.typ invoice.pdf
```
