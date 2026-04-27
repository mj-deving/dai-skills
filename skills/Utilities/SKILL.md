---
name: Utilities
description: Developer utilities — CLI generation, skill scaffolding, agent delegation, system upgrades, evals, documents, parsing, audio editing, Codex, Cloudflare, browser automation, prompting, aphorisms, n8n workflows, beads management, full output enforcement, knowledge base, compound engineering. USE WHEN create CLI, scaffold skill, delegate, upgrade system, eval, document, parse, cloudflare, browser, n8n, beads, full output, knowledge, compound engineering.
---

# Utilities

Unified skill for developer utility and tooling workflows.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Create CLI, build CLI, command-line tool, wrap API, TypeScript CLI, add command, upgrade tier | `CreateCLI/SKILL.md` |
| Create skill, new skill, scaffold skill, skill template, canonicalize, validate skill, update skill, fix skill structure | `CreateSkill/SKILL.md` |
| Parallel execution, agent teams, delegate, 3+ workstreams, agent specialization, swarm | `Delegation/SKILL.md` |
| Upgrade, improve system, check Anthropic, system upgrade, analyze for improvements, new Claude features, algorithm upgrade, mine reflections, find sources, research upgrade, PAI upgrade | `PAIUpgrade/SKILL.md` |
| Eval, evaluate, test agent, benchmark, verify behavior, regression test, capability test, run eval, compare models, compare prompts, create judge, view results | `Evals/SKILL.md` |
| Document, process file, create document, convert format, extract text, PDF, DOCX, XLSX, PPTX, Word, Excel, spreadsheet, PowerPoint, slides, consulting report, large PDF, merge PDF, fill form, tracked changes, redlining | `Documents/SKILL.md` |
| Parse, extract, URL, transcript, entities, JSON, batch, YouTube, PDF content, article, newsletter, Twitter, browser extension, collision detection, detect content type, extract article, extract YouTube, parse content | `Parser/SKILL.md` |
| Clean audio, edit audio, remove filler words, clean podcast, remove ums, cut dead air, polish audio, transcribe, analyze audio, audio pipeline | `AudioEditor/SKILL.md` |
| Ask codex, consult codex, codex review, codex audit, codexbridge, run codex, codex plan review, codex json output | `CodexBridge/SKILL.md` |
| Cloudflare, worker, deploy, Pages, MCP server, wrangler, DNS, KV, R2, D1, Vectorize | `Cloudflare/SKILL.md` |
| Browser, screenshot, debug web, verify UI, troubleshoot frontend, automate browser, browse website, review stories, run stories, web automation | `Browser/SKILL.md` |
| Meta-prompting, template generation, prompt optimization, programmatic prompt composition, render template, validate template, prompt engineering | `Prompting/SKILL.md` |
| Aphorism, quote, saying, find quote, research thinker, newsletter quotes, add aphorism, search aphorisms | `Aphorisms/SKILL.md` |
| Create PDF, generate PDF, CV, resume, cover letter, application letter, report PDF, proposal, invoice, typst, professional document, academic paper, letterhead | `Typst/SKILL.md` |
| Context audit, usage audit, token waste, context bloat, check settings, why is Claude slow, token optimization | `ContextAudit/SKILL.md` |
| n8n, n8n workflow, build workflow, n8n node, n8n expression, n8n validation, n8n code node, n8n pattern, n8n MCP, automation workflow, n8n template, webhook workflow, batch processing, n8n agent, n8n javascript, n8n python, workflow architecture | `n8n/SKILL.md` |
| Beads bootstrap, beads adopt, beads init, beads setup, standardize beads workflow | `../Beads/Bootstrap/SKILL.md` |
| Beads hook audit, beads hooks, inspect hooks, repair hooks, hook doctrine | `../Beads/HookAudit/SKILL.md` |
| Beads upgrade, beads tier, upgrade T1 to T2, upgrade T2 to T3, beads workflow evolution | `../Beads/UpgradePath/SKILL.md` |
| Full output, no truncation, complete code, no placeholders, exhaustive output | `FullOutput/SKILL.md` |
| Save to knowledge, search knowledge, recall, knowledge base, kn | `Knowledge/SKILL.md` |
| Compound engineering, multi-platform sync, sync to opencode/codex/gemini/copilot | `CompoundEngineering/SKILL.md` |

## Examples

**Example 1:** `User: "[typical request]"` → Routes to appropriate sub-skill workflow

**Example 2:** `User: "[another request]"` → Routes to different sub-skill workflow
