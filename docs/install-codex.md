# Install For Codex

Set `CODEX_HOME` if needed:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
```

Symlink selected skills:

```bash
ln -sfn "$PWD/skills/Beads" "$CODEX_HOME/skills/beads"
ln -sfn "$PWD/skills/Utilities/Browser" "$CODEX_HOME/skills/browser"
ln -sfn "$PWD/skills/Utilities/Browser/RealBrowserAttach" "$CODEX_HOME/skills/browser-real"
ln -sfn "$PWD/skills/Research" "$CODEX_HOME/skills/research"
ln -sfn "$PWD/skills/ProjectTelos" "$CODEX_HOME/skills/project-telos"
```

For Beads leaf skills:

```bash
ln -sfn "$PWD/skills/Beads/Bootstrap" "$CODEX_HOME/skills/beads-bootstrap"
ln -sfn "$PWD/skills/Beads/VersionAudit" "$CODEX_HOME/skills/beads-version-audit"
ln -sfn "$PWD/skills/Beads/HookAudit" "$CODEX_HOME/skills/beads-hook-audit"
ln -sfn "$PWD/skills/Beads/UpgradePath" "$CODEX_HOME/skills/beads-upgrade-path"
```

Restart Codex after adding symlinks so the skill list refreshes.
