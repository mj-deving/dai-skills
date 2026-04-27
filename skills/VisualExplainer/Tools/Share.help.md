# Share Tool

Share a visual explainer HTML file via Cloudflare Pages deployment.

## Usage
```bash
bash ${CLAUDE_SKILL_DIR}/Tools/Share.sh <html-file> [project-name]
```

## Arguments
- `html-file` — Path to the HTML file to share (required)
- `project-name` — Cloudflare Pages project name (default: `ve-shared`)

## Output
- **Live URL** — Public `*.pages.dev` URL for the shared diagram
- **Dashboard** — Link to Cloudflare Pages dashboard for the project
- **JSON** — `{"url":"...","project":"..."}` for programmatic use

## One-Time Setup
1. Create a free Cloudflare account at https://cloudflare.com
2. Run `npx wrangler login` (opens browser for OAuth)
3. Share diagrams — no further auth needed

## How It Works
1. Copies your HTML file as `index.html` to a temp directory
2. Deploys to Cloudflare Pages via `wrangler pages deploy`
3. Auto-creates the project if it doesn't exist
4. Returns a public `*.pages.dev` URL

## Free Tier
- 500 deploys/month
- Unlimited bandwidth
- Global CDN (300+ edge locations)
