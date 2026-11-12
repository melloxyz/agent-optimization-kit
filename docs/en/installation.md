# Installation and removal

[Português](../pt-BR/installation.md) | [Home](../../README.en.md)

Requires Windows PowerShell 5.1+, Python 3.10+ via `py -3` and Git. The other optimization tools are optional.

~~~powershell
.\scripts\doctor.ps1
.\scripts\stats.ps1
~~~

There is no account, background daemon or npm installer.

## Install global hooks

Default is **preview only** for Claude Code and Codex; no existing hooks are removed.

~~~powershell
.\scripts\install-context-guard.ps1
.\scripts\install-context-guard.ps1 -Agent Claude,Codex
# After checking the preview:
.\scripts\install-context-guard.ps1 -Apply
~~~

Gemini CLI is experimental and opt-in:

~~~powershell
.\scripts\install-context-guard.ps1 -Agent Gemini
.\scripts\install-context-guard.ps1 -Agent Gemini -Apply
~~~

`AfterModel` can fire for streaming chunks, adding Python startup overhead. Benchmark it before leaving it enabled.

The installer edits only user-level hook files (`~/.claude/settings.json`, `~/.codex/hooks.json`, `~/.gemini/settings.json`) and backs up each original file. It does not touch RTK, Headroom, Graphify, proxies or authentication.

## Remove only this kit's hook entries

~~~powershell
.\scripts\install-context-guard.ps1 -Remove
.\scripts\install-context-guard.ps1 -Remove -Apply
.\scripts\install-context-guard.ps1 -Agent Gemini -Remove -Apply
~~~

The installed command contains the absolute path to the Python file. Uninstall before moving this repository, then re-install from its new location.

## Validate

~~~powershell
py -3 -m unittest discover -s tests -v
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 349999
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 350000
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 400000
~~~

Use `-ConfigRoot` with a disposable profile for installer testing, never actual personal settings as test fixtures.

## Resume work

From the coding project's working directory:

~~~powershell
py -3 "C:\path\agent-optimization-kit\hooks\context-guard\context_guard.py" status
py -3 "C:\path\agent-optimization-kit\hooks\context-guard\context_guard.py" resume
~~~

Paste the resume prompt into the next agent session. No automatic process launch or elevated permissions. See [compatibility](compatibility.md).
