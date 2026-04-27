# Evidence-first bead template

## Description

Include:
- what is failing
- why it matters
- what outcome is needed

## Context

Include:
- repro commands or trigger path
- exact files or subsystems touched
- current observations
- constraints or known non-goals

## Notes

Include:
- `SOURCES: ...`
- `kn entry: ...`

## Acceptance criteria

Good criteria:
- prove the bug is fixed
- or prove the current theory is wrong

## Example skeleton

```text
Title: Reproduce and isolate lock contention in embedded Beads workspace

Description:
- repeated serialized writes succeed, but longer multi-command runs leave a lingering Dolt lock
- we need a reproducible explanation before enabling parallel mutations

Context:
- repro with: bd create ... followed by additional write commands in the same session
- observed evidence: later commands report database locked by another dolt process
- likely surface: embedded mode write lifecycle or process cleanup

Acceptance:
- either a stable repro exists with a documented workaround
- or the current theory is disproved and replaced with a better one
```
