# Agent Optimization Kit

[Português (BR)](README.md) | **English**

A small, public, reproducible setup for **making coding agents more efficient**. The repository documents tools, hooks, commands, diagnostics and measured results. It includes a lightweight continuity helper called **Context Guard**.

This is **not** a new agent, another proxy, a dashboard, or a way to bypass usage limits.

## What's included

| Component | Purpose | Status |
| --- | --- | --- |
| [RTK](https://github.com/rtk-ai/rtk) | Compact terminal command output | Used in the reference setup |
| [Headroom](https://github.com/headroomlabs-ai/headroom) | Context optimization through a proxy | Used with Codex in the reference setup |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Structural code knowledge graph | Used in the reference setup |
| **Context Guard** | 350k-token checkpoint and 400k-token handoff preparation | Initial opt-in implementation |
| **Doctor / Stats** | Inspect tools, hooks and measured savings in the terminal | Local scripts |

Context Guard **does not reset a five-hour plan allowance**. It creates a checkpoint when reliable context data is available, then helps an agent resume in a fresh session. The agent must complete and verify the checkpoint: the script never invents decisions or completed work.

## Quick start (Windows terminal)

Requirements: **PowerShell 5.1+**, **Python 3.10+**, and **Git**. The measured tools are optional.

~~~powershell
cd "$HOME\Desktop\agent-optimization-kit"
.\scripts\doctor.ps1
.\scripts\stats.ps1
.\scripts\stats.ps1 -Json
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 350000
py -3 -m unittest discover -s tests -v
~~~

Preview hook installation before changing anything:

~~~powershell
.\scripts\install-context-guard.ps1
# Apply only after reviewing the preview:
.\scripts\install-context-guard.ps1 -Apply
# Gemini CLI adapter is optional and requires real-world validation:
.\scripts\install-context-guard.ps1 -Agent Gemini
~~~

The installer defaults to **Claude Code and Codex**. No global hooks were modified while creating this repository. See the [installation guide](docs/en/installation.md).

## Context Guard

At **350,000 tokens**, it creates a checkpoint and asks the agent to record verified progress, user decisions and the next action. At **400,000 tokens**, it flags handoff and recommends a fresh session once the checkpoint is validated.

Thresholds can be configured, with a smaller-window fallback when model context size is known. It does **not** kill processes, force a restart, elevate permissions or call an LLM. See [design and safeguards](docs/en/context-guard.md).

## Reference setup observed on 2026-11-12

| Tool | Observed version |
| --- | --- |
| RTK | 1.1.0 |
| Headroom | 0.42.0 |
| Graphify | 0.9.102 |
| Claude Code | 2.1.322 |
| Codex CLI | 0.167.2 |
| Gemini CLI | 0.68.0 |
| OpenCode | 2.2.7 |

**RTK:** 2,413 processed commands, roughly **585.1k tokens removed (43.0%)** over the available lifetime measurements.

**Headroom:** **1,001,672 tokens removed over the last 30 days**, reported as **7.1% of new input**, not 7.1% of the plan quota.

**Do not add the numbers together.** The reporting periods and denominators differ. These are tool-reported measurements, not controlled effectiveness claims. Read [benchmark methodology](docs/en/benchmarks.md).

## Documentation

- [Installation and removal](docs/en/installation.md)
- [Tools and commands](docs/en/tools.md)
- [Agent and frontend compatibility](docs/en/compatibility.md)
- [Context Guard and safeguards](docs/en/context-guard.md)
- [Benchmarks and methodology](docs/en/benchmarks.md)
- [Documentação em Português](docs/pt-BR/installation.md)

## Privacy and contributing

This repository publishes **sanitized examples and original implementation code**, not private configuration exports. Never commit credentials, authentication material, transcripts, session history or private checkpoints. Checkpoints live outside the repository in local user data.

[MIT](LICENSE) for original project code; third-party projects retain their respective licenses. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

**Current status:** initial testable kit. Each integration must be explicitly enabled and validated. Universal compatibility and plan quota savings are not guaranteed.
