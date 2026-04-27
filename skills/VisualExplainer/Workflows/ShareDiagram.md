# ShareDiagram Workflow

<!-- Voice DEACTIVATED
```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the ShareDiagram workflow in the VisualExplainer skill"}' \
  > /dev/null 2>&1 &
```
-->

---

Share a visual explainer HTML file via Cloudflare Pages.

## Usage

```bash
bash ${CLAUDE_SKILL_DIR}/Tools/Share.sh <file-path> [project-name]
```

**Arguments:**
- `file-path` — Path to the HTML file to share (required)
- `project-name` — Cloudflare Pages project name (default: `ve-shared`)

**Examples:**
```bash
bash ${CLAUDE_SKILL_DIR}/Tools/Share.sh ${AGENT_HOME}/diagrams/my-diagram.html
bash ${CLAUDE_SKILL_DIR}/Tools/Share.sh ${AGENT_HOME}/diagrams/auth-flow.html auth-review
```

## How It Works

1. Copies your HTML file to a temp directory as `index.html`
2. Deploys to Cloudflare Pages via `wrangler pages deploy`
3. Auto-creates the project if it doesn't exist
4. Returns a public `*.pages.dev` URL

## One-Time Setup

If not yet authenticated with Cloudflare:
1. Create a free account at https://cloudflare.com
2. Run `npx wrangler login`

## Output

```
Sharing my-diagram.html...

✓ Shared successfully!

Live URL:  https://abc123.ve-shared.pages.dev
Project:   ve-shared
Dashboard: https://dash.cloudflare.com/?to=/:account/pages/view/ve-shared
```

JSON for programmatic use:
```json
{"url":"https://abc123.ve-shared.pages.dev","project":"ve-shared"}
```

## Notes

- Deployments are **public** — anyone with the URL can view
- Free tier: 500 deploys/month, unlimited bandwidth, global CDN
- Each deploy overwrites the previous one in the same project
- Use different project names to keep multiple diagrams live simultaneously
