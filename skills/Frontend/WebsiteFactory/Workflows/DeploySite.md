# DeploySite Workflow

Deploy a website to Netlify (free hosting with global CDN).

## Step 1: Verify Site is Ready

Check that the site directory contains:
- `index.html` (main page)
- Any assets (images, videos, fonts)
- No broken references (all paths relative)

## Step 2: Install Netlify CLI

```bash
npm install -g netlify-cli
```

If already installed, skip.

## Step 3: Login

```bash
netlify login
```

Opens browser for OAuth. Only needed once.

## Step 4: Deploy

### New Site

```bash
cd /path/to/site
netlify init
# Choose: Create & configure a new site
# Team: [your team]
# Site name: [choose or auto-generate]

netlify deploy --prod --dir .
```

### Existing Site (redeploy)

```bash
cd /path/to/site
netlify deploy --prod --dir .
```

### Via Claude Code

```
Deploy this website to Netlify. Run netlify deploy --prod --dir .
Show me the live URL when done.
```

## Step 5: Custom Domain (Optional)

```bash
netlify domains:add www.yourdomain.com
```

Then update DNS at your registrar:
- CNAME: `www` → `[site-name].netlify.app`
- Or: A record → Netlify's load balancer IP

## Step 6: Verify

1. Open the live URL
2. Test on mobile
3. Check Lighthouse score: `npx lighthouse [URL] --view`

## Netlify Free Tier Limits

| Feature | Limit |
|---|---|
| Hosting | Free forever |
| CDN | Global edge network |
| Bandwidth | 100 GB/month |
| Deploy previews | Unlimited |
| Custom domains | Yes |
| HTTPS | Automatic (Let's Encrypt) |

## Alternatives

| Platform | Free Tier | Best For |
|---|---|---|
| **Netlify** | 100 GB bandwidth | Default choice |
| **Vercel** | 100 GB bandwidth | Next.js / React |
| **GitHub Pages** | Unlimited (static) | Simple sites |
| **Cloudflare Pages** | Unlimited bandwidth | High-traffic |
