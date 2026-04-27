# Recovery drill

Run this on a disposable clone or test repo whenever possible.

## 1. Capture baseline

- repo root
- current `bd ready --json`
- configured Dolt remotes
- relevant `.beads/` files
- hook check output if hooks matter

## 2. Verify backup posture

Confirm that there is a known way to preserve or recreate Beads state before destructive experimentation.

## 3. Rehearse sync

For remote-backed repos:
- pull
- perform a harmless write if appropriate
- push
- verify another clone can observe the result

## 4. Rehearse lock recovery

If the environment has shown embedded lock or lingering-process symptoms:
- capture active `bd` or `dolt` processes
- serialize writes
- confirm the cleanup path and safe retry posture

## 5. Rehearse rebuild path

Know what happens if the local state is unusable:
- fresh clone
- reattach remote if needed
- restore hooks if they are machine-dependent
- verify that the queue is visible again

## Pass criteria

- each drill step has a known operator action
- no critical step depends on guesswork
- the report names what is still unverified
