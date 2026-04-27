#!/usr/bin/env bun
/**
 * algorithm-rules.test.ts — Eval Suite 1: Algorithm Rules Behavioral Validation
 *
 * Runs real Claude sessions via `claude -p` and grades whether Algorithm spec
 * rules actually change agent behavior.
 *
 * COST: ~$20-40 per full run (8 tasks × 3 trials × $0.50-2.00 each)
 *
 * Usage:
 *   bun test Tests/algorithm-rules.test.ts                     # full run
 *   DRY_RUN=1 bun test Tests/algorithm-rules.test.ts           # validate YAMLs only
 *   EVAL_TASKS=task_run_tests_first bun test ...               # single task
 *   EVAL_TRIALS=1 bun test ...                                 # reduce trial count
 *   EVAL_MODEL=sonnet bun test ...                             # use different model
 */

import { describe, test, expect, beforeAll } from 'bun:test';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'fs';
import { join, basename } from 'path';
import { parse as parseYaml } from 'yaml';
import {
  executeClaudeSession,
  getToolCallNames,
  wasToolCalled,
  wasSkillInvoked,
  getAssistantText,
  type ExecutorResult,
} from '../Tools/ClaudeExecutor.ts';

// ── Config ─────────────────────────────────────────

const EVALS_DIR = join(import.meta.dir, '..');
const TASKS_DIR = join(EVALS_DIR, 'UseCases', 'Regression');
const RESULTS_DIR = join(EVALS_DIR, 'Results', 'algorithm-rules');
const SUITE_PATH = join(EVALS_DIR, 'Suites', 'Regression', 'algorithm-rules.yaml');

const DRY_RUN = process.env.DRY_RUN === '1';
const EVAL_TASKS = process.env.EVAL_TASKS?.split(',');
const EVAL_TRIALS = parseInt(process.env.EVAL_TRIALS ?? '0'); // 0 = use task default
const EVAL_MODEL = process.env.EVAL_MODEL; // optional model override

// ── Types ──────────────────────────────────────────

interface TaskDef {
  id: string;
  description: string;
  prompt: string;
  setup?: {
    working_dir?: string;
    prepare?: string;
  };
  graders: GraderDef[];
  trials: number;
  pass_threshold: number;
  max_turns?: number;
  max_budget_usd?: number;
  tags?: string[];
}

interface GraderDef {
  type: string;
  weight: number;
  required?: boolean;
  params?: Record<string, unknown>;
}

interface TrialResult {
  trial: number;
  score: number;
  passed: boolean;
  toolsCalled: string[];
  costUsd: number;
  durationMs: number;
  graderResults: { grader: string; score: number; reasoning: string }[];
}

interface TaskResult {
  taskId: string;
  trials: TrialResult[];
  passRate: number;
  meanScore: number;
  totalCostUsd: number;
  passed: boolean;
}

// ── Helpers ────────────────────────────────────────

function loadSuite(): string[] {
  const suite = parseYaml(readFileSync(SUITE_PATH, 'utf-8'));
  return suite.tasks;
}

function loadTask(taskId: string): TaskDef {
  const path = join(TASKS_DIR, `${taskId}.yaml`);
  if (!existsSync(path)) throw new Error(`Task file not found: ${path}`);
  return parseYaml(readFileSync(path, 'utf-8')) as TaskDef;
}

async function prepareWorkspace(task: TaskDef): Promise<void> {
  if (!task.setup?.prepare) return;

  const cwd = task.setup.working_dir ?? '${TMPDIR}/eval-workspace';
  const proc = Bun.spawn(['bash', '-c', task.setup.prepare], {
    cwd: existsSync(cwd) ? cwd : '/tmp',
    stdout: 'pipe',
    stderr: 'pipe',
  });
  await proc.exited;
}

async function gradeWithToolCalls(
  result: ExecutorResult,
  graderParams: Record<string, unknown>
): Promise<{ score: number; reasoning: string }> {
  const toolNames = getToolCallNames(result.transcript);
  const checks: { name: string; passed: boolean }[] = [];

  // Check required tools
  const required = graderParams.required as { tool: string; params?: Record<string, unknown> }[] | undefined;
  if (required) {
    for (const req of required) {
      const toolPattern = req.tool;
      if (toolPattern.includes('*')) {
        // Glob match
        const re = new RegExp('^' + toolPattern.replace(/\*/g, '.*') + '$', 'i');
        const found = result.transcript.tool_calls.some(tc => {
          if (!re.test(tc.name)) return false;
          if (req.params) {
            for (const [k, v] of Object.entries(req.params)) {
              const actual = String(tc.params[k] ?? '');
              const expected = String(v);
              if (expected.includes('*')) {
                if (!new RegExp('^' + expected.replace(/\*/g, '.*') + '$', 'i').test(actual)) return false;
              } else if (actual !== expected) return false;
            }
          }
          return true;
        });
        checks.push({ name: `required:${toolPattern}`, passed: found });
      } else {
        let found: boolean;
        if (req.params) {
          found = result.transcript.tool_calls.some(tc => {
            if (tc.name !== req.tool) return false;
            for (const [k, v] of Object.entries(req.params!)) {
              const actual = String(tc.params[k] ?? '');
              const expected = String(v);
              if (expected.includes('*')) {
                if (!new RegExp('^' + expected.replace(/\*/g, '.*') + '$', 'i').test(actual)) return false;
              } else if (!actual.toLowerCase().includes(expected.toLowerCase())) return false;
            }
            return true;
          });
        } else {
          found = wasToolCalled(result.transcript, req.tool);
        }
        checks.push({ name: `required:${req.tool}`, passed: found });
      }
    }
  }

  // Check forbidden tools
  const forbidden = graderParams.forbidden as string[] | undefined;
  if (forbidden) {
    for (const f of forbidden) {
      checks.push({ name: `forbidden:${f}`, passed: !wasToolCalled(result.transcript, f) });
    }
  }

  // Check sequence — supports "Edit|Write" alternatives with pipe separator
  const sequence = graderParams.sequence as string[] | undefined;
  if (sequence) {
    let seqIdx = 0;
    for (const name of toolNames) {
      if (seqIdx < sequence.length) {
        const alternatives = sequence[seqIdx].split('|');
        if (alternatives.some(alt => alt.trim() === name)) {
          seqIdx++;
        }
      }
    }
    checks.push({ name: `sequence:${sequence.join('→')}`, passed: seqIdx === sequence.length });
  }

  const passCount = checks.filter(c => c.passed).length;
  const score = checks.length > 0 ? passCount / checks.length : 0;
  const reasoning = checks.map(c => `${c.passed ? '✅' : '❌'} ${c.name}`).join(', ');

  return { score, reasoning: `${passCount}/${checks.length}: ${reasoning}` };
}

async function gradeWithLLMRubric(
  result: ExecutorResult,
  graderParams: Record<string, unknown>
): Promise<{ score: number; reasoning: string }> {
  const rubric = graderParams.rubric as string;
  const scale = (graderParams.scale as string) ?? '1-5';
  const maxScore = parseInt(scale.split('-')[1] ?? '5');

  // Use claude -p to grade the transcript
  const assistantText = getAssistantText(result.transcript);
  const toolsSummary = getToolCallNames(result.transcript).join(', ');

  const gradePrompt = `You are an eval grader. Grade this agent transcript against the rubric.

RUBRIC:
${rubric}

AGENT TOOL CALLS (in order):
${toolsSummary || 'none'}

AGENT OUTPUT (truncated):
${assistantText.slice(0, 3000)}

Respond with ONLY a JSON object: {"score": N, "reasoning": "brief explanation"}
Score must be ${scale}.`;

  try {
    const gradeResult = await executeClaudeSession({
      prompt: gradePrompt,
      maxTurns: 1,
      maxBudgetUsd: 0.10,
      timeoutMs: 30_000,
      model: 'haiku',
    });

    const gradeText = getAssistantText(gradeResult.transcript);
    // Extract JSON from response
    const jsonMatch = gradeText.match(/\{[^}]*"score"\s*:\s*(\d+)[^}]*"reasoning"\s*:\s*"([^"]+)"[^}]*\}/);
    if (jsonMatch) {
      const score = parseInt(jsonMatch[1]) / maxScore;
      return { score, reasoning: jsonMatch[2] };
    }

    // Fallback: try to find just a number
    const numMatch = gradeText.match(/\b([1-5])\b/);
    if (numMatch) {
      return { score: parseInt(numMatch[1]) / maxScore, reasoning: 'Score extracted from text' };
    }

    return { score: 0.5, reasoning: 'Could not parse grader output' };
  } catch (e) {
    return { score: 0.5, reasoning: `Grader error: ${e}` };
  }
}

async function gradeResult(
  result: ExecutorResult,
  graders: GraderDef[]
): Promise<{ score: number; graderResults: { grader: string; score: number; reasoning: string }[] }> {
  const graderResults: { grader: string; score: number; reasoning: string }[] = [];
  let weightedSum = 0;
  let totalWeight = 0;

  for (const grader of graders) {
    let gradeOutput: { score: number; reasoning: string };

    if (grader.type === 'tool_calls') {
      gradeOutput = await gradeWithToolCalls(result, grader.params ?? {});
    } else if (grader.type === 'llm_rubric') {
      gradeOutput = await gradeWithLLMRubric(result, grader.params ?? {});
    } else {
      gradeOutput = { score: 0.5, reasoning: `Unsupported grader type: ${grader.type}` };
    }

    const weight = grader.weight ?? 1.0;
    weightedSum += gradeOutput.score * weight;
    totalWeight += weight;

    graderResults.push({
      grader: grader.type,
      score: gradeOutput.score,
      reasoning: gradeOutput.reasoning,
    });
  }

  return {
    score: totalWeight > 0 ? weightedSum / totalWeight : 0,
    graderResults,
  };
}

async function runTask(task: TaskDef): Promise<TaskResult> {
  const trialCount = EVAL_TRIALS || task.trials || 3;
  const trials: TrialResult[] = [];

  // Prepare workspace
  await prepareWorkspace(task);

  for (let i = 0; i < trialCount; i++) {
    console.log(`  Trial ${i + 1}/${trialCount}...`);

    // Re-prepare workspace for each trial (clean state)
    await prepareWorkspace(task);

    const result = await executeClaudeSession({
      prompt: task.prompt,
      maxTurns: task.max_turns ?? 10,
      maxBudgetUsd: task.max_budget_usd ?? 1.0,
      timeoutMs: 180_000,
      cwd: task.setup?.working_dir ?? '${TMPDIR}/eval-workspace',
      model: EVAL_MODEL,
    });

    const { score, graderResults } = await gradeResult(result, task.graders);
    const passed = score >= (task.pass_threshold ?? 0.60);

    trials.push({
      trial: i + 1,
      score,
      passed,
      toolsCalled: getToolCallNames(result.transcript),
      costUsd: result.costUsd,
      durationMs: result.durationMs,
      graderResults,
    });

    console.log(`    ${passed ? '✅' : '❌'} Score: ${(score * 100).toFixed(0)}% | Tools: ${getToolCallNames(result.transcript).slice(0, 5).join(', ')} | $${result.costUsd.toFixed(2)}`);
  }

  const passCount = trials.filter(t => t.passed).length;
  const passRate = passCount / trialCount;
  const meanScore = trials.reduce((sum, t) => sum + t.score, 0) / trialCount;
  const totalCostUsd = trials.reduce((sum, t) => sum + t.costUsd, 0);

  return {
    taskId: task.id,
    trials,
    passRate,
    meanScore,
    totalCostUsd,
    passed: passRate >= (task.pass_threshold ?? 0.60),
  };
}

// ── Test Suite ─────────────────────────────────────

describe('Algorithm Rules — Eval Suite 1', () => {
  let taskIds: string[];
  let allResults: TaskResult[];

  beforeAll(() => {
    taskIds = EVAL_TASKS ?? loadSuite();
    allResults = [];

    if (!existsSync(RESULTS_DIR)) {
      mkdirSync(RESULTS_DIR, { recursive: true });
    }
  });

  if (DRY_RUN) {
    test('all task YAMLs parse correctly', () => {
      const ids = EVAL_TASKS ?? loadSuite();
      for (const id of ids) {
        const task = loadTask(id);
        expect(task.id).toBe(id);
        expect(task.prompt).toBeTruthy();
        expect(task.graders.length).toBeGreaterThan(0);
        console.log(`  ✅ ${id}: ${task.graders.length} graders, ${task.trials} trials, $${task.max_budget_usd ?? 1.0}/trial`);
      }
      console.log(`\n  Total tasks: ${ids.length}`);
      const maxCost = ids.reduce((sum, id) => {
        const t = loadTask(id);
        return sum + (t.max_budget_usd ?? 1.0) * (t.trials ?? 3);
      }, 0);
      console.log(`  Max cost estimate: $${maxCost.toFixed(2)}`);
    });

    return;
  }

  // Generate one test per task
  const ids = EVAL_TASKS ?? loadSuite();
  for (const taskId of ids) {
    test(taskId, async () => {
      console.log(`\n📋 ${taskId}`);
      const task = loadTask(taskId);
      const result = await runTask(task);
      allResults.push(result);

      // Save result
      const resultPath = join(RESULTS_DIR, `${taskId}-${Date.now()}.json`);
      writeFileSync(resultPath, JSON.stringify(result, null, 2));

      console.log(`  Result: ${result.passed ? '✅ PASS' : '❌ FAIL'} | pass@k: ${(result.passRate * 100).toFixed(0)}% | mean: ${(result.meanScore * 100).toFixed(0)}% | cost: $${result.totalCostUsd.toFixed(2)}`);

      // Eval tests always pass — they record baselines, not enforce gates.
      // Check results in Results/algorithm-rules/ for actual scores.
      expect(result.trials.length).toBeGreaterThan(0);
    }, 600_000); // 10 min timeout per task
  }
});
