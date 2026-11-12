#!/usr/bin/env python3
"""Context Guard: small, opt-in context checkpoints for coding agents.

Standard library only. No network calls, model calls, process termination or
automatic session launching. Hook failures never block an agent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

WARNING_DEFAULT = 350_000
HANDOFF_DEFAULT = 400_000
LEVELS = {"normal": 0, "warning": 1, "handoff": 2}


def home() -> Path:
    configured = os.environ.get("AGENT_KIT_HOME")
    base = configured or os.environ.get("LOCALAPPDATA")
    return (Path(base) / "agent-optimization-kit" if base and not configured
            else Path(base).expanduser() if configured
            else Path.home() / ".agent-optimization-kit")


def limits(window: int | None = None) -> tuple[int, int]:
    warning = int(os.environ.get("CONTEXT_GUARD_WARNING", str(WARNING_DEFAULT)))
    handoff = int(os.environ.get("CONTEXT_GUARD_HANDOFF", str(HANDOFF_DEFAULT)))
    if not (0 < warning < handoff):
        raise ValueError("warning must be less than handoff")
    if window and window < handoff:
        return min(warning, int(window * 0.75)), min(handoff, int(window * 0.90))
    return warning, handoff


def level_for(tokens: int, window: int | None = None) -> str:
    warn, handoff = limits(window)
    return "handoff" if tokens >= handoff else "warning" if tokens >= warn else "normal"


def claude_usage_from_transcript(path: str) -> int | None:
    """Last usage record, not total tokens spent across the entire session."""
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            end = f.tell()
            f.seek(max(0, end - 2_000_000))
            data = f.read().decode("utf-8", errors="replace")
        if end > 2_000_000:
            data = data.split("\n", 1)[-1]
        for line in reversed(data.splitlines()):
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if entry.get("type") != "assistant":
                continue
            usage = (entry.get("message") or {}).get("usage")
            if isinstance(usage, dict) and isinstance(usage.get("input_tokens"), int):
                return sum(int(usage.get(key) or 0) for key in (
                    "input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    except (OSError, UnicodeError):
        pass
    return None


def read_tokens(payload: dict, agent: str) -> tuple[int | None, str]:
    if agent == "claude":
        usage = (payload.get("message") or {}).get("usage") or payload.get("usage")
        if isinstance(usage, dict) and isinstance(usage.get("input_tokens"), int):
            return sum(int(usage.get(k) or 0) for k in (
                "input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")), "claude-usage"
        transcript = payload.get("transcript_path")
        return (claude_usage_from_transcript(transcript), "claude-transcript") if transcript else (None, "unavailable")
    if agent == "codex":
        usage = payload.get("token_usage")
        # For Codex, input_tokens normally already includes the cached portion.
        # Never add cached_input_tokens again.
        if isinstance(usage, dict) and isinstance(usage.get("input_tokens"), int):
            return usage["input_tokens"], "codex-post-model-input"
    if agent == "gemini":
        usage = (payload.get("llm_response") or {}).get("usageMetadata") or {}
        for key, source in (("promptTokenCount", "gemini-prompt"),
                            ("totalTokenCount", "gemini-total-estimate")):
            if isinstance(usage.get(key), int):
                return usage[key], source
    return None, "unavailable"


def key_for(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def paths(agent: str, cwd: Path, session: str) -> tuple[Path, Path]:
    project_id = key_for(str(cwd.resolve()).casefold())
    session_id = key_for(agent + ":" + session)
    base = home() / "context-guard" / project_id / session_id
    return base / "state.json", base / "STATUS.md"


def git_facts(cwd: Path) -> str:
    def run(*args: str) -> str:
        try:
            result = subprocess.run(["git", "-C", str(cwd), *args],
                                    capture_output=True, text=True, timeout=3,
                                    encoding="utf-8", errors="replace")
            return result.stdout.strip() if result.returncode == 0 else "unavailable"
        except (OSError, subprocess.TimeoutExpired):
            return "unavailable"
    commit = run("rev-parse", "--short", "HEAD")
    status = run("status", "--short")
    lines = status.splitlines()
    summary = "\n".join(lines[:40]) or "(working tree clean or unavailable)"
    if len(lines) > 40:
        summary += f"\n... {len(lines) - 40} more entries"
    return f"Commit: {commit}\n\nGit status:\n{summary}"


def make_checkpoint(path: Path, agent: str, cwd: Path, tokens: int, source: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    body = (f"# Context Guard | Session checkpoint\n\n"
            f"Generated: {stamp}\n\nAgent: {agent}\n\n"
            f"Project: {cwd}\n\nObserved context: {tokens:,} tokens ({source})\n\n"
            "## Objective\n\n[Agent: describe the current user-approved objective]\n\n"
            "## Verified progress\n\n[Agent: state completed work with evidence]\n\n"
            "## Decisions and constraints\n\n[Agent: preserve explicit user decisions]\n\n"
            "## Work in progress and running processes\n\n"
            "[Agent: describe active tasks; never terminate them merely for handoff]\n\n"
            "## Tests and verification\n\n[Agent: include commands and actual results]\n\n"
            "## Next exact action\n\n[Agent: specify one concrete next step]\n\n"
            "## Git facts (automatically collected)\n\n" + git_facts(cwd) + "\n")
    path.write_text(body, encoding="utf-8")


def load_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(temp, path)


def notice(stage: str, checkpoint: Path) -> str:
    base = f"Context Guard ({stage.upper()}): checkpoint local em {checkpoint}. "
    if stage == "warning":
        return base + ("Atualize objetivo, progresso verificado, decisões, testes e próximo passo "
                       "no STATUS.md. Continue a tarefa atual com economia de contexto.")
    return base + ("Complete e valide o STATUS.md antes de iniciar trabalho novo. "
                   "Não mate processos em execução. Recomende uma sessão limpa e "
                   "retomada pelo arquivo, sem elevar permissões ou lançar agentes automaticamente.")


def handle(payload: dict, agent: str) -> dict:
    event = payload.get("hook_event_name", "")
    cwd = Path(payload.get("cwd") or os.getcwd()).resolve()
    session = str(payload.get("session_id") or payload.get("sessionId") or "unknown")
    state_path, checkpoint_path = paths(agent, cwd, session)
    state = load_state(state_path)
    tokens, source = read_tokens(payload, agent)
    previous_level = state.get("level", "normal")
    current_level = previous_level
    changed = False
    if tokens is not None and tokens >= 0:
        raw_window = os.environ.get("CONTEXT_GUARD_MODEL_WINDOW")
        window = int(raw_window) if raw_window and raw_window.isdigit() else None
        measured = level_for(tokens, window)
        if LEVELS[measured] > LEVELS[previous_level]:
            current_level = measured
            make_checkpoint(checkpoint_path, agent, cwd, tokens, source)
            changed = True
        state.update(agent=agent, project=str(cwd), level=current_level,
                     last_tokens=tokens, token_source=source,
                     checkpoint=str(checkpoint_path),
                     updated_utc=datetime.now(timezone.utc).isoformat())
        save_state(state_path, state)

    prompt_events = {"UserPromptSubmit", "BeforeAgent"}
    is_prompt = event in prompt_events
    should_notify = (is_prompt and LEVELS[current_level] >
                     LEVELS.get(state.get("notified", "normal"), 0))
    if should_notify:
        state["notified"] = current_level
        save_state(state_path, state)
    message = notice(current_level, checkpoint_path) if current_level != "normal" else ""
    if agent == "gemini":
        if should_notify:
            return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": message}}
        return {}
    if should_notify:
        return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": message}}
    if changed and event in {"Stop", "PostModelRequest"}:
        # Only UI feedback; model receives actionable context at next prompt.
        if agent == "codex":
            return {}
        return {"systemMessage": message}
    return {}


def last_state(cwd: Path) -> tuple[dict, Path | None]:
    base = home() / "context-guard" / key_for(str(cwd.resolve()).casefold())
    found = sorted(base.glob("*/state.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return (load_state(found[0]), found[0]) if found else ({}, None)


def main() -> int:
    parser = argparse.ArgumentParser(description="Lightweight context checkpoints; no service required")
    sub = parser.add_subparsers(dest="command", required=True)
    hook = sub.add_parser("hook", help="Read one JSON hook event from stdin")
    hook.add_argument("--agent", choices=("claude", "codex", "gemini"), required=True)
    sim = sub.add_parser("simulate", help="Preview thresholds without writing files")
    sim.add_argument("--tokens", type=int, required=True)
    sim.add_argument("--window", type=int, default=None)
    sub.add_parser("status", help="Latest checkpoint for current directory")
    sub.add_parser("resume", help="Print a safe resume prompt for current directory")
    args = parser.parse_args()

    if args.command == "simulate":
        warn, handoff = limits(args.window)
        print(f"context={args.tokens:,}; warning={warn:,}; handoff={handoff:,}; "
              f"state={level_for(args.tokens, args.window)}")
        return 0
    if args.command in ("status", "resume"):
        state, file = last_state(Path.cwd())
        if file is None:
            print("No checkpoint for this directory.")
            return 1
        checkpoint = state.get("checkpoint")
        if args.command == "status":
            print(f"agent={state.get('agent')} level={state.get('level')} "
                  f"tokens={state.get('last_tokens')} source={state.get('token_source')}")
            print(f"checkpoint={checkpoint}")
        else:
            print(f'Read "{checkpoint}", verify current git status and tests, '
                  'then continue the recorded next step. Do not assume unverified '
                  'claims are complete. Request permission for any sensitive action.')
        return 0
    try:
        payload = json.load(sys.stdin)
        output = handle(payload, args.agent)
        if output or args.agent == "gemini":
            print(json.dumps(output, ensure_ascii=False))
    except Exception as exc:
        if os.environ.get("CONTEXT_GUARD_DEBUG") == "1":
            print(f"Context Guard: {type(exc).__name__}: {exc}", file=sys.stderr)
        if args.agent == "gemini":
            print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
