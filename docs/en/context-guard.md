# Context Guard

[Português](../pt-BR/context-guard.md) | [Home](../../README.en.md)

A small local checkpoint/resume helper. It does not compress the transcript directly or reset plan limits.

## Behavior

- **350,000 tokens:** create a local `STATUS.md` with Git facts and placeholders for the agent to complete; notify once per threshold level and session.
- **400,000 tokens:** flag handoff and recommend a fresh session once the checkpoint is verified. Never kill processes, elevate privileges or automatically launch another agent.
- **Resume:** `status` and `resume` expose the checkpoint path and next-session prompt.
- **Fail open:** missing counters and parsing errors never block agent actions.

For smaller context windows set `CONTEXT_GUARD_MODEL_WINDOW`. Below 400k, warning/handoff are capped at 75%/90% of the declared window.

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `CONTEXT_GUARD_WARNING` | 350000 | Warning threshold |
| `CONTEXT_GUARD_HANDOFF` | 400000 | Handoff threshold |
| `CONTEXT_GUARD_MODEL_WINDOW` | Unset | Model window for proportionate thresholds |
| `AGENT_KIT_HOME` | User-local data | Local state and checkpoints |
| `CONTEXT_GUARD_DEBUG` | 0 | Optional fail-open diagnostic output |

~~~powershell
$env:CONTEXT_GUARD_MODEL_WINDOW = '200000'
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 180000 --window 200000
~~~

## Local data and privacy

On Windows, private state normally lives under `%LOCALAPPDATA%\agent-optimization-kit\context-guard\...`. Project and session folders use hashed identifiers. The script does **not** copy transcripts, prompts or tool outputs. Checkpoints may still contain a project path and Git filenames: **never publish private checkpoints**.

The first checkpoint contains placeholders. An agent must supply and verify objective, decisions, tests, evidence and the next step. Unverified statements must not be treated as completed work.

## Limits

Measurements reflect a recent model call/response, **not cumulative subscription usage**. Hook schemas may change. Codex uses `PostModelRequest` rather than unstable transcript parsing; Gemini may rely on an estimate.

There is no automatic session restart, hard blocking of tools, history deletion or new agent launch. Run offline tests and try a disposable project before global activation.
