# Workflow templates

## Canary then batch rollout

Parent:
- roll out service across host fleet

Children:
- inventory and prerequisites
- automation preparation
- canary host rollout
- human findings gate
- batch rollout
- burn-in and promotion review

## Bug investigation

Parent:
- resolve reported failure

Children:
- reproduce
- collect evidence
- isolate likely surface
- patch
- regression proof
- close or supersede contradictory beads

## Incident recovery

Parent:
- recover service safely

Children:
- detect and classify
- collect logs and state snapshot
- immediate containment
- recovery action
- verification gate
- follow-up bead creation

## Long refactor

Parent:
- complete bounded refactor program

Children:
- epic per directory or subsystem
- task per file or bounded module
- review gate every logical batch

Use these as shapes, not rigid law.
