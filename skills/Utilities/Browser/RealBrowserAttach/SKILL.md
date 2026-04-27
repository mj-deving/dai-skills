---
name: RealBrowserAttach
description: Attach to a real existing browser session instead of launching a separate Linux or WSL browser. Use when the user wants their current logged-in browser, real Brave on Windows from WSL, existing browser session, native messaging, CDP attach, remote debugging port, RunBrowser, Browserbase attach strategy, or Interceptor comparison.
---

# Real Browser Attach

Use this side-skill when the goal is to control the user's real browser context rather than an isolated automation browser.

## Routing

Prefer this skill over generic browser automation when the request includes any of:
- "real browser"
- "existing browser"
- "logged-in browser"
- "Windows browser"
- "Brave"
- "attach to Chrome"
- "native messaging"
- "remote debugging port"
- "CDP"
- "RunBrowser"
- "Interceptor"

## Core Doctrine

The substrate comes first. Do not start with Browserbase `autobrowse`, Playwright, or a headless Linux browser when the user explicitly wants the browser they already use.

Choose in this order:
1. **Native-messaging host via `wsl.exe` stdio for real Brave**
   Current primary build target. This is the PAI-owned path for driving the already-running Brave profile on Windows with zero network exposure.
2. **`dbalabka/chrome-wsl` bridge**
   Validation and fallback path for real Chrome/CDP workflows. Useful baseline, but no longer the main roadmap driver.
3. **Extension relay fallback**
   Use `mcp-chrome` first, then RunBrowser if needed. These remain contingency substrates if the native-messaging path stalls.
4. **Mirrored networking or manual portproxy**
   Experimental and last-resort. Only use after the higher-confidence paths fail and only with explicit validation of networking side effects.
5. **Browserbase remote/browser automation**
   Use for isolated sessions, bot-protected sites, or cloud automation. Do not treat it as the default answer to "use my real browser."

## Current Guidance For This Machine

Read these references before deciding the implementation:
- [tooling-comparison.md](references/tooling-comparison.md)
- [windows-attach.md](references/windows-attach.md)

The current local findings matter:
- Browserbase `browse` is not the canonical real-browser path here.
- Interceptor is useful conceptually, but is currently macOS-only.
- Windows Chrome CDP can run, but WSL attachment is not plug-and-play on this machine.
- The active build decision is now: native-messaging relay for real Brave first; all CDP bridge paths are fallback-only.

## Workflow

### 1. Confirm the target browser surface

Decide whether the user wants:
- the actual daily browser/profile
- a disposable Windows browser
- an isolated cloud browser

If they want the real daily browser on this machine, bias to the native-messaging Brave relay first.

### 2. Pick the substrate

Use this decision rule:
- **Real existing Brave browser on this machine**: build or extend the native-messaging relay path first
- **Need a comparison baseline or fallback**: try `chrome-wsl`
- **Need a third-party real-browser fallback**: prefer `mcp-chrome`, then RunBrowser
- **Need cross-machine or bot-resistant automation**: Browserbase remote
- **Need standards-based debugging and the boundary is controllable**: direct CDP attach only after proven connectivity

### 3. Validate the boundary before promising success

For WSL plus Windows browser:
- do not assume `127.0.0.1:9222` in WSL reaches Windows Chrome
- do not assume `--remote-debugging-address=0.0.0.0` will expose Chrome beyond Windows localhost
- empirically test connectivity first

If CDP is chosen, validate:
```bash
curl -fsS http://<target>:9222/json/version
curl -fsS http://<target>:9222/json/list
```

If those fail, stop calling it a CDP solution and switch to:
- the native-messaging relay if it is the target path
- `chrome-wsl` if a fallback baseline is needed
- an extension relay
- a Windows-side proxy/forwarding layer

### 4. Keep agent compatibility unified

This workflow should work for both Claude and Codex:
- avoid Claude-only slash-command assumptions
- avoid Codex-only home-path assumptions in user-facing doctrine
- keep the browser strategy in PAI-owned skills, not in ad hoc local notes

### 5. Position Browserbase correctly

Browserbase `autobrowse` is an optional training loop once the browser substrate is healthy.

It is **not** the first thing to deploy when:
- the user wants the real browser
- the browser is on Windows and the agent is in WSL
- the goal is to preserve logins, cookies, tabs, and extensions

Browserbase `ui-test` is an optional adversarial testing layer once the same substrate is healthy.

For the current roadmap, both Browserbase layers sit downstream of the native-messaging Brave relay rather than competing with it.

## Output Expectations

When you use this skill, produce:
- the chosen substrate and why
- the exact blocker if attachment is not yet possible
- the next concrete step to make it real

Do not say "browser automation is installed" if the agent still cannot reach the intended browser surface.
