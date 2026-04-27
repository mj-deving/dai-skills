---
name: graphify
description: "any input (code, docs, papers, images) - knowledge graph - clustered communities - HTML + JSON + audit report"
trigger: /graphify
---

# /graphify

Turn any folder of files into a navigable knowledge graph with community detection, an honest audit trail, and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language `GRAPH_REPORT.md`.

Use this skill when the user asks to turn code, docs, papers, images, videos, notes, or a mixed corpus into a persistent knowledge graph; query an existing graph; find paths between concepts; add a URL to a graph corpus; export graph artifacts; or run graphify watch/hooks/Claude integration.

## Usage

```bash
/graphify                                             # full pipeline on current directory -> Obsidian vault
/graphify <path>                                      # full pipeline on specific path
/graphify <path> --mode deep                          # thorough extraction, richer INFERRED edges
/graphify <path> --update                             # incremental - re-extract only new/changed files
/graphify <path> --directed                           # preserve edge direction: source -> target
/graphify <path> --cluster-only                       # rerun clustering on existing graph
/graphify <path> --no-viz                             # skip visualization, just report + JSON
/graphify <path> --svg                                # also export graph.svg
/graphify <path> --graphml                            # export graph.graphml
/graphify <path> --neo4j                              # generate graphify-out/cypher.txt
/graphify <path> --mcp                                # start MCP stdio server for agent access
/graphify <path> --watch                              # watch folder, auto-rebuild on code changes
/graphify <path> --wiki                               # build agent-crawlable wiki
/graphify add <url>                                   # fetch URL, save to ./raw, update graph
/graphify query "<question>"                          # BFS traversal - broad context
/graphify path "AuthModule" "Database"                # shortest path between concepts
/graphify explain "SwinTransformer"                   # plain-language node explanation
```

## Why It Exists

graphify follows the `/raw` folder workflow: drop anything into a folder — papers, tweets, screenshots, code, notes — and get a structured graph that shows what is connected.

Three things it does that a model alone cannot reliably provide:

1. **Persistent graph** — relationships are stored in `graphify-out/graph.json` and survive across sessions.
2. **Honest audit trail** — every edge is tagged `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`.
3. **Cross-document surprise** — community detection finds relationships across files that the user may not know to ask about.

Use it for new codebases, reading lists, research corpora, and personal raw folders.

## Progressive Loading

Read only the file needed for the requested path:

| Request shape | Read next |
|---|---|
| Full `/graphify` pipeline, including install, file detection, and transcription | [`SetupAndDetection.md`](SetupAndDetection.md), then [`Extraction.md`](Extraction.md), then [`GraphOutputs.md`](GraphOutputs.md) |
| Entity/relationship extraction details, AST extraction, semantic subagents, caching, or merge logic | [`Extraction.md`](Extraction.md) |
| Clustering, community labels, HTML, Obsidian, wiki, Neo4j, SVG, GraphML, MCP, benchmark, manifest, and final report | [`GraphOutputs.md`](GraphOutputs.md) |
| `--update` or `--cluster-only` | [`IncrementalOps.md`](IncrementalOps.md) |
| `query`, `path`, or `explain` | [`QueryOps.md`](QueryOps.md) |
| `add`, `--watch`, commit hook, or Claude integration | [`AutomationOps.md`](AutomationOps.md) |
| Edge provenance, cost visibility, warning, and reporting constraints | [`HonestyRules.md`](HonestyRules.md) |

For normal full-pipeline invocation, follow the referenced files in order and do not skip steps.

## Core Rules

- If no path was given, use `.` and do not ask for a path.
- Never invent an edge. If unsure, use `AMBIGUOUS`.
- Never skip the corpus-size warning.
- Always show token cost in the report.
- Never hide cohesion scores behind symbols; show the raw number.
- Never run HTML visualization on a graph with more than 5,000 nodes without warning the user.
- Preserve the interpreter guard: subsequent commands must use `$(cat graphify-out/.graphify_python)` after setup.
- For semantic extraction, use parallel extraction agents as described in [`Extraction.md`](Extraction.md); do not read all files manually one by one.
