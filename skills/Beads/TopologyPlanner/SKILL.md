---
name: beads-topology-planner
description: Choose the right Beads collaboration topology. USE WHEN deciding between embedded single-clone, shared-remote clones, per-clone remotes, or server mode for concurrent writers.
---

# Beads Topology Planner

Use this skill when the question is not "how do I use Beads?" but "which Beads operating shape fits this collaboration model?"

Outcome rule:
- recommend the smallest topology that fits
- make tradeoffs explicit
- give a concrete command sketch, not only theory

## Workflow

1. Read [references/topology-matrix.md](references/topology-matrix.md).
2. Collect only the facts that matter:
   - how many active agents or humans write at once
   - one clone or multiple clones/worktrees
   - whether everyone must see one shared queue
   - whether isolated branches/remotes are acceptable
   - whether true multi-writer access is required
3. If the environment is unclear, run `beads-version-audit` first.
4. Produce:
   - recommended topology
   - why smaller options fail
   - minimal command or setup sketch

## Default decision bias

- solo or one active writer: embedded single clone
- multiple clones, shared visibility, no true multi-writer need: shared remote
- many agents, low conflict tolerance, no need for one global queue: per-clone remotes
- true concurrent writers to one repo state: server mode

Do not recommend server mode just because it sounds advanced.
