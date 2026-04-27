# Output Schemas

## Default Findings Schema

{"summary":"string","findings":[{"severity":"high|medium|low","title":"string","details":"string","refs":["path:line"]}],"questions":["string"],"next_steps":["string"]}

## Plan Review Schema

{"summary":"string","findings":[{"severity":"high|medium|low","title":"string","details":"string","refs":["path:line"]}],"questions":["string"],"sequence_risks":["string"],"missing_tests":["string"]}

## Repo Audit Schema

{"summary":"string","findings":[{"severity":"high|medium|low","title":"string","details":"string","refs":["path:line"]}],"security":["string"],"reliability":["string"],"test_gaps":["string"],"next_steps":["string"]}

## Validation Rule

- JSON output must parse with `jq .`
- If parsing fails, re-run with stricter instruction: "Return ONLY valid minified JSON"
