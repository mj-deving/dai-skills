# Topology matrix

## 1. Embedded single clone

Use when:
- one active writer at a time
- local or low-complexity repo

Pros:
- simplest setup
- least operational overhead

Cons:
- no safe multi-writer posture
- durability depends on local repo plus optional remote sync

## 2. Embedded with shared remote across clones

Use when:
- several agents or machines need a shared view
- each agent has its own clone or worktree
- writes are still effectively serialized by clone-level workflows

Pros:
- shared visibility into issues and progress
- familiar pull/push model

Cons:
- rejected pushes and sync conflicts are part of normal life
- everyone needs pull discipline

## 3. Embedded with separate remote per clone

Use when:
- many agents run in parallel
- conflict avoidance matters more than one global queue
- later aggregation or maintainer oversight is acceptable

Pros:
- low push conflict pressure
- strong isolation

Cons:
- no single shared issue view by default
- coordination moves up a level

## 4. Server mode

Use when:
- true concurrent writers are required
- one shared live database is operationally acceptable

Pros:
- designed for real multi-writer access

Cons:
- more moving parts
- needs stronger operational discipline and recovery planning

## Decision questions

- Do multiple writers need to mutate the same Beads state concurrently?
- Is one shared queue required, or is federated visibility acceptable?
- Are agents in separate clones or the same working copy?
- Is the team prepared to run and recover a server?

When in doubt, choose the smaller topology and document the escalation trigger for moving up.
