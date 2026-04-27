#!/usr/bin/env bun
/**
 * Sync.ts — Distribute PAI global ${AGENT_HOME}/ config to other AI tools
 *
 * Wraps compound-plugin CLI `sync` command.
 * This pushes PAI's global skills, commands, and settings OUTWARD to other tools.
 * It does NOT sync compound skills — for that, use Install.ts.
 *
 * Usage: bun Sync.ts [target]
 *   target: opencode | codex | droid | cursor | pi | copilot | gemini | kiro | windsurf | openclaw | qwen | all
 */

import { resolveCliContext, runCompoundCli, validateTarget } from "./shared";

async function main() {
  const args = process.argv.slice(2);
  const target = args[0] ? validateTarget(args[0]) : "all";
  const { compoundHome, cliEntry, bunPath } = resolveCliContext();

  console.log(`Syncing PAI config to ${target}...`);
  console.log(`  Direction: ${AGENT_HOME}/ -> other AI tools`);

  await runCompoundCli(bunPath, cliEntry, ["sync", target], {
    cwd: compoundHome,
    timeout: 60_000,
    label: `Sync to ${target}`,
  });
}

main();
