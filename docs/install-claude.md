# Install For Claude

The simplest local install is a symlink from Claude's skills directory to this repo:

```bash
mkdir -p "$HOME/.claude/skills"
ln -sfn "$PWD/skills/Beads" "$HOME/.claude/skills/Beads"
ln -sfn "$PWD/skills/Utilities/Browser" "$HOME/.claude/skills/Browser"
```

For a broad install, copy or symlink specific category folders. Avoid blindly installing local/private skills until they are reviewed.

If using Beads hooks, run the relevant Beads setup checks inside each target repo:

```bash
bd setup claude --check || true
bd setup codex --check || true
```
