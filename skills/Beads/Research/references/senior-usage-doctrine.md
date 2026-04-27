# Senior usage doctrine

These patterns show up repeatedly in the strongest source material and in high-signal upstream usage.

## 1. Use Beads as the durable execution graph

Strong users do not treat Beads as a generic note bucket. They use it to hold:
- task boundaries
- dependencies
- gates and waits
- handoff state
- evidence and provenance

## 2. Make tasks small and explicit

The most convincing public example is Dustin Brown's long-running refactor workflow:
- epic per directory
- bead per file or bounded unit
- manual review gates between major batches

This is the antidote to agents shortcutting large refactors.

## 3. Raise issue quality at creation time

High-signal beads include:
- the problem and why it matters
- exact repro commands when known
- observed evidence
- likely fix surface
- acceptance criteria that could prove the theory wrong

This matches the strongest upstream usage patterns and should be the default for investigations and bugs.

## 4. Clean stale plans aggressively

Senior users do not preserve dead epics for sentimental reasons. They supersede, close, or invalidate stale work once better evidence exists.

## 5. Choose the smallest topology that fits

Server mode, federation, and other advanced features are justified by real collaboration pressure, not by aesthetics. The power-user move is not "use every feature"; it is "choose the smallest durable model that avoids conflict and ambiguity."

## 6. Treat recovery as a normal workflow

Backups, pull/push, mode mismatch, stale locks, and remote drift should all have a known drill. If recovery is only considered during failure, the setup is incomplete.
