#!/usr/bin/env bun
/**
 * Install.ts — Convert compound plugin to other AI tool formats
 *
 * Wraps compound-plugin CLI `install` command.
 * This converts compound's plugin content (skills, agents) INTO another tool's format.
 * It does NOT sync PAI globals — for that, use Sync.ts.
 *
 * Usage: bun Install.ts <plugin-name> --to <target> [--output <path>]
 *   plugin-name: compound-engineering (or other plugin name)
 *   target: opencode | codex | droid | cursor | pi | copilot | gemini | kiro | windsurf | openclaw | qwen | all
 */

import { VALID_TARGETS, resolveCliContext, runCompoundCli, validateTarget } from "./shared";

const PATH_SEPARATOR = /[/\\]/;

function validatePluginName(input: string): string {
  const cleaned = input.trim();
  if (PATH_SEPARATOR.test(cleaned)) {
    console.error(`Error: Plugin name cannot contain path separators: ${input}`);
    process.exit(1);
  }
  if (cleaned.length === 0 || cleaned.length > 100) {
    console.error(`Error: Plugin name must be 1-100 characters.`);
    process.exit(1);
  }
  return cleaned;
}

function parseArgs(argv: string[]): { plugin: string; target: string; output?: string } {
  const args = argv.slice(2);
  let plugin = "";
  let target = "";
  let output: string | undefined;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--to" && args[i + 1]) {
      target = args[++i];
    } else if ((args[i] === "--output" || args[i] === "-o") && args[i + 1]) {
      output = args[++i];
    } else if (!args[i].startsWith("--") && !plugin) {
      plugin = args[i];
    }
  }

  if (!plugin || !target) {
    console.error("Usage: bun Install.ts <plugin-name> --to <target> [--output <path>]");
    console.error("Example: bun Install.ts compound-engineering --to codex");
    console.error(`Valid targets: ${VALID_TARGETS.join(", ")}`);
    process.exit(1);
  }

  return { plugin, target, output };
}

async function main() {
  const { plugin, target, output } = parseArgs(process.argv);
  const validatedPlugin = validatePluginName(plugin);
  const validatedTarget = validateTarget(target);
  const { compoundHome, cliEntry, bunPath } = resolveCliContext();

  console.log(`Installing ${validatedPlugin} for ${validatedTarget}...`);
  console.log(`  Direction: compound plugin -> ${validatedTarget} format`);

  const cliArgs = ["install", validatedPlugin, "--to", validatedTarget];
  if (output) {
    cliArgs.push("--output", output);
  }

  await runCompoundCli(bunPath, cliEntry, cliArgs, {
    cwd: compoundHome,
    timeout: 120_000,
    label: `Install of ${validatedPlugin} to ${validatedTarget}`,
  });
}

main();
