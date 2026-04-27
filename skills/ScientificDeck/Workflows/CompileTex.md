# CompileTex Workflow

Fix LaTeX compilation errors and warnings.

## Trigger
"compile tex", "fix latex", "latex errors"

## Steps

### Step 1: Locate .tex file

### Step 2: Compile
```bash
pdflatex -interaction=nonstopmode <file>.tex 2>&1
```

### Step 3: Parse warnings/errors with line numbers

### Step 4: Fix iteratively — minimal changes, recompile after each

### Step 5: Verify zero-warning compile
```bash
pdflatex -interaction=nonstopmode <file>.tex 2>&1 | grep -cE "Warning|Error|Overfull|Underfull"
# Must return: 0
```
