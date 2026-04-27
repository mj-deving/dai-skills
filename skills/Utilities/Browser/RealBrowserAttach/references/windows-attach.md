# Windows Browser Attach Notes

These notes capture the current empirical findings for Windows Chrome from WSL.

## What was proven

- Windows Chrome can be started with a remote debugging port.
- Windows itself can reach that listener on `127.0.0.1`.
- WSL could not reach the Windows Chrome CDP listener via `127.0.0.1:9222`.
- WSL also could not reach the listener via the default Windows host gateway IP.
- Launching Chrome with `--remote-debugging-address=0.0.0.0` still resulted in a Windows-local listener only in the observed test.

## Meaning

Direct WSL -> Windows Chrome CDP is not safe to assume on this machine.

If you need a real Windows browser, plan for one of:
- an extension relay
- a Windows-side proxy or forwarding layer
- a Windows-native agent process

Do not frame raw CDP as "already working" unless these pass from WSL:

```bash
curl -fsS http://<target>:9222/json/version
curl -fsS http://<target>:9222/json/list
```

## Practical Doctrine

- For the active roadmap, prefer the native-messaging relay for real Brave.
- Treat raw CDP as an advanced fallback that requires explicit validation.
- Treat Browserbase remote as separate from real-browser attachment.

## 2026-04-23 update — research-informed path

Further research (see
`~/projects/Pai-Exploration/docs/real-browser-substrate-wsl-windows-2026-04-23.md`)
demoted mirrored mode from primary because of open 2025 regressions on
exactly the Tailscale + Docker stack this machine runs. The current
recommendation is:

1. **Native-messaging host for real Brave** (Anthropic pattern, validated on
   WSL2 in anthropics/claude-code#41625) — current PAI build target and
   architectural winner.
2. **`dbalabka/chrome-wsl`** — purpose-built WSL↔Windows Chrome bridge. Keep as
   fallback and comparison baseline.
3. **`hangwin/mcp-chrome`** — 11.3k-star extension relay, third-party fallback.
4. **Mirrored mode** — experimental, reversible. Only after Paths 1–3 have
   failed and only after auditing Docker and Tailscale impact.

Critical gotchas discovered:
- Chrome 111+ rejects non-loopback CDP connections with HTTP 403 unless
  launched with `--remote-allow-origins=<allowed or *>`. Silent killer of most
  naive portproxy setups.
- `/json/version` returns a `webSocketDebuggerUrl` containing `localhost:9222`;
  WSL clients must rewrite that host before passing to `connectOverCDP`, or
  Playwright/Puppeteer will dial WSL's own localhost and fail.
- Mirrored mode silently port-locks ~4000 high ports on Windows
  (microsoft/WSL#40169) and `ignoredPorts` does not rescue it.
- Chrome M113+ forces `--remote-debugging-address=0.0.0.0` back to loopback;
  bridge on the Windows side, not on the Chrome side.
