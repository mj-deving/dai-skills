# Failure Modes

## 1. Invalid JSON Output

Symptoms:
- trailing prose outside JSON
- markdown fences around JSON
- malformed quotes

Recovery:
1. Re-run in `-j` mode
2. prepend strict instruction: "Return ONLY valid minified JSON"
3. validate with `jq .`

## 2. Over-broad Autonomous Execution

Symptoms:
- Codex attempts risky operations without explicit approval intent

Recovery:
1. remove `--auto`
2. split task into analysis first, action second
3. require `--confirm-risk` for high-impact prompts
4. use --scope to constrain file modifications: --scope 'src/foo.ts,src/bar.ts'
5. after --auto runs, verify with: git diff --stat (only scoped files should appear)

## 3. Weak Prompt Specificity

Symptoms:
- vague findings
- missing file refs
- generic summaries

Recovery:
1. specify output contract
2. include scope and risk focus
3. request severity ordering and concrete refs

## 4. Repo Context Drift

Symptoms:
- task run in wrong repo
- references unrelated files

Recovery:
1. always pass `-C <repo>`
2. echo planned command before run
3. include repo path in prompt context when needed

## 5. Token Exhaustion Before Final Answer

Symptoms:
- Codex reads many files or logs and never emits the requested findings block
- output ends mid-analysis or with an incomplete summary
- tests may have run, but the final contract is missing
- **Most common cause: input exceeds ~300 lines without a findings-first contract**

Recovery:
1. **Split the input by concern area** — each chunk under 300 lines
2. **Add findings-first output contract** to every prompt (see PromptTemplates.md)
3. **Concatenate prompt + focused diff** into a single -f file
4. **Run focused reviews in parallel** — one per concern area
5. Narrow scope to exact files, dirs, or diff
6. Prefer `-j` mode for reviews that need deterministic structure
7. Split broad tasks into triage first, deep dive second

Evidence: Full 1900-line diff → 65K tokens consumed, zero findings. Same diff split into 3 focused chunks (225, 229, 180 lines) with findings-first contract → 13 findings across 3 parallel reviews, 10 fixed.
