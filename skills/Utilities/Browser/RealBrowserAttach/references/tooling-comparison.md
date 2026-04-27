# Tooling Comparison

## Browserbase `browse` / `autobrowse`

Strengths:
- strong for isolated browser automation
- good fit for remote/browserbase-hosted sessions
- `autobrowse` adds an iterative strategy-improvement loop

Limits for this use case:
- upstream `autobrowse` is Claude-oriented
- it assumes the browser substrate is already healthy
- local `browse` is not the same thing as "use my real Windows browser"

Use when:
- cloud or isolated automation is acceptable
- bot resistance matters more than using the user's current browser
- you are training a reusable browser workflow after the substrate is stable

## RunBrowser

Strengths:
- built around the real browser, not a spawned automation browser
- extension relay avoids a lot of raw WSL-to-Windows CDP friction
- preserves logins, cookies, extensions, and visible tabs
- better fit for "use my actual browser"

Limits:
- requires extension installation and local relay setup
- not the same ecosystem as Browserbase

Use when:
- the user wants their real logged-in Windows browser
- the agent is in WSL but the browser is on Windows
- collaboration with the visible browser matters

## Interceptor

Strengths:
- strong conceptual model for real-browser and human-in-the-loop workflows
- richer than plain CDP in several areas
- avoids the "spawn a second browser" model entirely

Limits:
- currently macOS-only
- not a direct install target for this Windows/WSL machine

Use when:
- designing doctrine for real-browser control

Do not use when:
- you need a Windows implementation right now

## Canonical Recommendation

Revised 2026-04-23 after research pass (see
`~/projects/Pai-Exploration/docs/real-browser-substrate-wsl-windows-2026-04-23.md`),
then recentered the same day after the roadmap decision shifted to a PAI-owned
relay for the user's real Brave browser.

For this machine and this roadmap:

1. **Native-messaging host with `wsl.exe` stdio bridge for real Brave** —
   current primary build target. PAI-owned, zero network exposure, and aligned
   with the user's decision to target the already-running Brave profile.
2. **`dbalabka/chrome-wsl` bridge** — purpose-built npm tool for WSL↔Windows
   Chrome. Keep as a comparison baseline and fallback if the native-messaging
   relay stalls.
3. **`hangwin/mcp-chrome`** (11.3k stars, Dec 2025) — third-party extension
   relay, strong fallback if both the native-messaging path and chrome-wsl are
   unsuitable.
4. **`networkingMode=mirrored` + `browse env local 9222`** — Microsoft's
   endorsed answer for the generic case, but has 2025 regressions with
   Tailscale (tailscale#14790) and Docker Desktop. Use only after auditing.
5. **Windows `netsh portproxy` + `--remote-allow-origins=*`** — works but has
   sharp edges (Chrome 111 DNS-rebinding block, `webSocketDebuggerUrl` rewrite
   needed). `dbalabka/chrome-wsl` wraps this correctly.
6. **Browserbase remote** only for isolated/hostile-site workflows.

After the substrate is solved, layer Browserbase `autobrowse` (iterative
training) and `ui-test` (adversarial testing) on top of the same browser
control channel.
Interceptor remains out of scope on Windows/WSL — macOS-only today; its
native-messaging architecture is the inspiration for option 2.
