#!/usr/bin/env bun
/**
 * ClaudeExecutor.ts — Run Claude Code sessions and capture transcripts
 *
 * Executes `claude -p` with stream-json output, parses the JSONL into
 * the Evals Transcript format for grading.
 *
 * Usage:
 *   import { executeClaudeSession } from './ClaudeExecutor.ts';
 *   const result = await executeClaudeSession({
 *     prompt: "Update import paths in these 5 files...",
 *     maxTurns: 10,
 *     maxBudgetUsd: 0.50,
 *     timeoutMs: 120_000,
 *   });
 */

import type { Transcript, ToolCall, Turn, TranscriptMetrics } from '../Types/index.ts';

// ── Types ──────────────────────────────────────────

export interface ExecutorOptions {
  /** The prompt to send to Claude */
  prompt: string;
  /** Max conversation turns (default: 10) */
  maxTurns?: number;
  /** Max budget in USD (default: 1.00) */
  maxBudgetUsd?: number;
  /** Timeout in ms (default: 120_000) */
  timeoutMs?: number;
  /** Working directory for the session */
  cwd?: string;
  /** Additional CLI flags */
  extraFlags?: string[];
  /** Model override */
  model?: string;
}

export interface ExecutorResult {
  transcript: Transcript;
  rawEvents: StreamEvent[];
  costUsd: number;
  durationMs: number;
  exitCode: number;
  error?: string;
}

interface StreamEvent {
  type: string;
  subtype?: string;
  [key: string]: unknown;
}

interface ContentBlock {
  type: string;
  text?: string;
  name?: string;
  id?: string;
  input?: Record<string, unknown>;
}

interface ToolResultBlock {
  type: string;
  content?: string | ContentBlock[];
}

// ── Executor ───────────────────────────────────────

export async function executeClaudeSession(
  options: ExecutorOptions
): Promise<ExecutorResult> {
  const {
    prompt,
    maxTurns = 10,
    maxBudgetUsd = 1.0,
    timeoutMs = 120_000,
    cwd,
    extraFlags = [],
    model,
  } = options;

  const startTime = Date.now();
  const args = [
    'claude',
    '-p', prompt,
    '--output-format', 'stream-json',
    '--verbose',
    '--max-turns', String(maxTurns),
    '--max-budget-usd', String(maxBudgetUsd),
  ];

  if (model) {
    args.push('--model', model);
  }

  args.push(...extraFlags);

  const proc = Bun.spawn(args, {
    cwd: cwd ?? process.cwd(),
    stdout: 'pipe',
    stderr: 'pipe',
    env: { ...process.env },
  });

  // Set up timeout
  const timeout = setTimeout(() => {
    proc.kill();
  }, timeoutMs);

  let stdout = '';
  let stderr = '';
  try {
    [stdout, stderr] = await Promise.all([
      new Response(proc.stdout).text(),
      new Response(proc.stderr).text(),
    ]);
  } finally {
    clearTimeout(timeout);
  }

  const exitCode = await proc.exited;
  const durationMs = Date.now() - startTime;

  // Parse JSONL events
  const events = parseStreamJson(stdout);

  // Extract transcript
  const transcript = eventsToTranscript(events, prompt);

  // Extract cost from result event
  const resultEvent = events.find(e => e.type === 'result');
  const costUsd = (resultEvent?.total_cost_usd as number) ?? 0;

  return {
    transcript,
    rawEvents: events,
    costUsd,
    durationMs,
    exitCode,
    error: exitCode !== 0 ? stderr.slice(0, 500) : undefined,
  };
}

// ── Parsing ────────────────────────────────────────

function parseStreamJson(output: string): StreamEvent[] {
  const events: StreamEvent[] = [];
  for (const line of output.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    try {
      events.push(JSON.parse(trimmed));
    } catch {
      // Skip malformed lines
    }
  }
  return events;
}

function eventsToTranscript(events: StreamEvent[], prompt: string): Transcript {
  const turns: Turn[] = [];
  const toolCalls: ToolCall[] = [];
  const reasoningTraces: string[] = [];
  let turnIndex = 0;
  const startedAt = new Date().toISOString();

  // Add the initial user prompt
  turns.push({
    index: turnIndex++,
    role: 'user',
    content: prompt,
    timestamp: startedAt,
  });

  for (const event of events) {
    const type = event.type;

    if (type === 'assistant') {
      const message = event.message as { content?: ContentBlock[]; role?: string } | undefined;
      const content = message?.content ?? [];
      const textParts: string[] = [];

      if (Array.isArray(content)) {
        for (const block of content) {
          if (block.type === 'text' && block.text) {
            textParts.push(block.text);
          } else if (block.type === 'tool_use') {
            const tc: ToolCall = {
              id: block.id ?? `tc_${Date.now()}`,
              name: block.name ?? 'unknown',
              params: block.input ?? {},
              started_at: new Date().toISOString(),
            };
            toolCalls.push(tc);
          } else if (block.type === 'thinking' && block.text) {
            reasoningTraces.push(block.text);
          }
        }
      }

      if (textParts.length > 0) {
        turns.push({
          index: turnIndex++,
          role: 'assistant',
          content: textParts.join('\n'),
          timestamp: new Date().toISOString(),
        });
      }
    } else if (type === 'user') {
      // Tool results come back as user messages
      const message = event.message as { content?: ToolResultBlock[] } | undefined;
      const content = message?.content ?? [];
      let toolResultText = '';

      if (Array.isArray(content)) {
        for (const block of content) {
          if (block.type === 'tool_result') {
            const resultContent = block.content;
            if (typeof resultContent === 'string') {
              toolResultText += resultContent;
            } else if (Array.isArray(resultContent)) {
              for (const sub of resultContent) {
                if (sub.type === 'text' && sub.text) {
                  toolResultText += sub.text;
                }
              }
            }
          }
        }
      }

      if (toolResultText) {
        turns.push({
          index: turnIndex++,
          role: 'tool',
          content: toolResultText.slice(0, 2000), // Truncate large tool results
          timestamp: new Date().toISOString(),
        });
      }
    }
  }

  // Extract metrics from result event
  const resultEvent = events.find(e => e.type === 'result');
  const usage = resultEvent?.usage as {
    input_tokens?: number;
    output_tokens?: number;
    cache_read_input_tokens?: number;
    cache_creation_input_tokens?: number;
  } | undefined;

  const inputTokens = (usage?.input_tokens ?? 0) +
    (usage?.cache_read_input_tokens ?? 0) +
    (usage?.cache_creation_input_tokens ?? 0);
  const outputTokens = usage?.output_tokens ?? 0;

  const metrics: TranscriptMetrics = {
    n_turns: turns.length,
    n_tool_calls: toolCalls.length,
    total_tokens: inputTokens + outputTokens,
    input_tokens: inputTokens,
    output_tokens: outputTokens,
    wall_time_ms: (resultEvent?.duration_ms as number) ?? 0,
  };

  return {
    task_id: 'pending',
    trial_id: 'pending',
    started_at: startedAt,
    completed_at: new Date().toISOString(),
    turns,
    tool_calls: toolCalls,
    reasoning_traces: reasoningTraces.length > 0 ? reasoningTraces : undefined,
    metrics,
  };
}

// ── Helpers ────────────────────────────────────────

/** Extract just tool call names from a transcript — for quick grading */
export function getToolCallNames(transcript: Transcript): string[] {
  return transcript.tool_calls.map(tc => tc.name);
}

/** Check if a specific tool was called */
export function wasToolCalled(transcript: Transcript, toolName: string): boolean {
  return transcript.tool_calls.some(tc => tc.name === toolName);
}

/** Check if a Skill was invoked with a specific skill name */
export function wasSkillInvoked(transcript: Transcript, skillName: string): boolean {
  return transcript.tool_calls.some(tc => {
    if (tc.name !== 'Skill') return false;
    const skill = tc.params.skill as string | undefined;
    return skill?.toLowerCase().includes(skillName.toLowerCase());
  });
}

/** Get the full text output from assistant turns */
export function getAssistantText(transcript: Transcript): string {
  return transcript.turns
    .filter(t => t.role === 'assistant')
    .map(t => t.content)
    .join('\n');
}

/** Count ISC criteria in assistant output */
export function countISCCriteria(transcript: Transcript): number {
  const text = getAssistantText(transcript);
  const matches = text.match(/- \[ \] ISC-\d+:/g);
  return matches?.length ?? 0;
}

// ── CLI ────────────────────────────────────────────

if (import.meta.main) {
  const prompt = Bun.argv[2];
  if (!prompt) {
    console.log('Usage: ClaudeExecutor.ts "<prompt>" [--max-turns N] [--max-budget N]');
    process.exit(1);
  }

  const maxTurns = parseInt(Bun.argv[Bun.argv.indexOf('--max-turns') + 1] || '5');
  const maxBudget = parseFloat(Bun.argv[Bun.argv.indexOf('--max-budget') + 1] || '0.50');

  console.log(`Running: "${prompt.slice(0, 60)}..." (max ${maxTurns} turns, $${maxBudget} budget)`);

  const result = await executeClaudeSession({
    prompt,
    maxTurns,
    maxBudgetUsd: maxBudget,
  });

  console.log(`\nDone in ${result.durationMs}ms, cost $${result.costUsd.toFixed(4)}`);
  console.log(`Turns: ${result.transcript.turns.length}, Tool calls: ${result.transcript.tool_calls.length}`);
  console.log(`Tools used: ${getToolCallNames(result.transcript).join(', ') || 'none'}`);
}
