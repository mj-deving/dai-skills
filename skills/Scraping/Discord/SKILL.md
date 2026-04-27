---
name: discrawl
description: Discord guild archiving and search via discrawl CLI. USE WHEN Discord search, Discord history, Discord messages, Discord members, Discord channels, search Discord, Discord archive, Discord mentions, Discord server, Discord guild, discrawl.
---

# discrawl

Use `discrawl` to archive, search, and query Discord guild data locally. Read-only — for sending messages, use the Discord MCP plugin.

## Authentication

Requires a Discord bot token with **Message Content** and **Server Members** intents enabled in the Discord Developer Portal.

```bash
export DISCORD_BOT_TOKEN="your-bot-token"
```

```toml
# ~/.discrawl/config.toml
token_source = "env"
token_env = "DISCORD_BOT_TOKEN"
```

Run `discrawl doctor` to verify connectivity before any operation.

## First-Run Setup

```bash
discrawl init                        # create config
# Edit ~/.discrawl/config.toml → guild_id = "YOUR_GUILD_ID"
discrawl sync                        # full history backfill
discrawl search --json "hello"       # verify
```

## Quick Start

- `discrawl status` — sync status and database stats
- `discrawl doctor` — diagnostic check (connectivity, permissions, DB)
- `discrawl search "query"` — full-text search across messages
- `discrawl messages --channel general --limit 20` — recent messages
- `discrawl members` — list guild members with profiles
- `discrawl channels` — list all channels and threads
- `discrawl mentions --user 123456789` — find mentions of a user
- `discrawl sync` — incremental sync (new messages since last)
- `discrawl sync --full` — force complete history resync
- `discrawl tail` — live monitoring via Discord Gateway

## JSON Output (use for PAI consumption)

Add `--json` to any read command for structured output. Use `--plain` for TSV.

```bash
discrawl search --json "deployment issue"
discrawl messages --json --channel general --limit 10
discrawl members --json
discrawl mentions --json --user 123456789
```

## Search Modes

Default is FTS5 (fast, local). Optional: semantic (OpenAI embeddings) or hybrid. Configure in `~/.discrawl/config.toml` under `[search]` with `default_mode`, `embeddings_provider`, `embeddings_model`, `embeddings_api_key_env`.

## Message Filtering

```bash
discrawl messages --json --channel "dev" --author "alice" --since "24h" --limit 50
```

Flags: `--channel`, `--author`, `--since`, `--before`, `--limit`. All combinable.

## Live Monitoring (tail)

```bash
discrawl tail                        # foreground, real-time via Gateway
# Configure repair_every = "6h" in config.toml for consistency checks
```

For background daemon, create a systemd user service:

```ini
# ~/.config/systemd/user/discrawl-tail.service
[Unit]
Description=discrawl Discord live monitor
After=network-online.target

[Service]
ExecStart=%h/.local/bin/discrawl tail
Restart=on-failure
RestartSec=30
EnvironmentFile=%h/.config/discrawl/env

[Install]
WantedBy=default.target
```

Where `~/.config/discrawl/env` contains `DISCORD_BOT_TOKEN=your-token`.

## Direct SQL Access

Database: `~/.discrawl/db.sqlite`. Tables: `messages`, `members`, `channels`, `message_attachments`, `mention_events`.

```bash
discrawl sql "SELECT count(*) FROM messages"
discrawl sql --json "SELECT author_id, count(*) as n FROM messages GROUP BY author_id ORDER BY n DESC LIMIT 10"
sqlite3 ~/.discrawl/db.sqlite "SELECT * FROM messages WHERE content LIKE '%deploy%' LIMIT 5"
```

## Multi-Guild

```toml
guild_ids = ["111111111", "222222222"]
default_guild_id = "111111111"
```

Use `--guild` flag to target a specific guild. `discrawl sync --all` syncs all.

## Tips

- `--json` for PAI, `--plain` for piping, default for human reading
- `discrawl sync --since 24h` for quick incremental updates
- The SQLite DB is the real asset — query it directly for custom analysis
- Read-only tool — use Discord MCP plugin for send/react/edit
- Member search covers bios, pronouns, locations — not just usernames
- Concurrency: `concurrency = 16` in config.toml (range 8-32)
