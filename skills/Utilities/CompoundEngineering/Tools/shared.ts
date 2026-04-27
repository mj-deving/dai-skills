#!/usr/bin/env bun
/**
 * shared.ts — Common utilities for CompoundEngineering CLI tool wrappers
 *
 * Extracted to avoid duplication between Sync.ts and Install.ts.
 * Both tools delegate to the compound-plugin CLI via execFile.
 */

import { execFile } from "child_process";
import { homedir } from "os";
import { join, resolve } from "path";
import { promisify } from "util";

export const execFileAsync = promisify(execFile);

export const VALID_TARGETS = [
  "opencode",
  "codex",
  "droid",
  "cursor",
  "pi",
  "copilot",
  "gemini",
  "kiro",
  "windsurf",
  "openclaw",
  "qwen",
  "all",
] as const;

export type Target = (typeof VALID_TARGETS)[number];

export function resolveCompoundHome(): string {
  if (process.env.COMPOUND_HOME) {
    return resolve(process.env.COMPOUND_HOME.replace(/^~/, homedir()));
  }
  return join(homedir(), "projects", "compound-engineering-plugin");
}

export function validateTarget(input: string): Target {
  const cleaned = input.trim().toLowerCase();
  if (!VALID_TARGETS.includes(cleaned as Target)) {
    console.error(`Error: Unknown target "${input}".`);
    console.error(`Valid targets: ${VALID_TARGETS.join(", ")}`);
    process.exit(1);
  }
  return cleaned as Target;
}

/**
 * Resolve and validate the compound CLI entry point.
 * Returns { compoundHome, cliEntry, bunPath } or exits with a descriptive error.
 */
export function resolveCliContext(): { compoundHome: string; cliEntry: string; bunPath: string } {
  const compoundHome = resolveCompoundHome();
  const cliEntry = join(compoundHome, "src", "index.ts");
  const bunPath = process.execPath;
  return { compoundHome, cliEntry, bunPath };
}

/**
 * Run a compound CLI command via execFile. Handles errors with friendly messages.
 */
export async function runCompoundCli(
  bunPath: string,
  cliEntry: string,
  args: string[],
  opts: { cwd: string; timeout: number; label: string },
): Promise<void> {
  process.env.NODE_ENV = "production";
  try {
    const { stdout, stderr } = await execFileAsync(bunPath, [cliEntry, ...args], {
      cwd: opts.cwd,
      timeout: opts.timeout,
    });
    if (stdout) console.log(stdout);
    if (stderr) console.error(stderr);
    console.log(`${opts.label} complete.`);
  } catch (err: unknown) {
    if (err instanceof Error) {
      const code = (err as NodeJS.ErrnoException).code;
      if (code === "ETIMEDOUT") {
        console.error(`Error: ${opts.label} timed out after ${opts.timeout / 1000} seconds.`);
      } else if (code === "ENOENT") {
        console.error(`Error: CLI entry not found. Is compound-engineering-plugin installed at ${opts.cwd}?`);
        console.error(
          `Clone it: git clone https://github.com/EveryInc/compound-engineering-plugin ${opts.cwd}`,
        );
      } else {
        console.error(`Error: ${opts.label} failed.`);
        const stderr = (err as { stderr?: string }).stderr;
        console.error(stderr || err.message);
      }
    } else {
      console.error(`Error: ${opts.label} failed with unknown error.`);
    }
    process.exit(1);
  }
}
