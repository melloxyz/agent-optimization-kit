# Tools and commands

[Português](../pt-BR/tools.md) | [Home](../../README.en.md)

This kit documents a personal setup; it does not redistribute third-party binaries. Check each upstream license and documentation.

## RTK

Project: https://github.com/rtk-ai/rtk

RTK shortens terminal output before the agent reads it. The reference `rtk gain` output reported savings from `rg`, ESLint, Vitest and other commands.

~~~powershell
rtk --version
rtk gain
rtk --help
~~~

Windows WinGet package: `winget install rtk-ai.rtk`. Review upstream instructions before running `rtk init` to avoid duplicate hooks.

## Headroom

Project: https://github.com/headroomlabs-ai/headroom

Headroom can optimize context through a local proxy and reports its own measurements. In the observed setup it was routed to **Codex**, not Claude Code.

~~~powershell
headroom --version
headroom doctor
headroom savings
~~~

Installed does not imply routed. Check `headroom doctor` and avoid stacking proxies without measuring cache behavior.

## Graphify

Project: https://github.com/Graphify-Labs/graphify

Knowledge graph for structural code navigation. One graph was observed in DCR TUI; this does not prove every repository is indexed.

~~~powershell
graphify --version
graphify --help
~~~

Graphify is not a direct token compressor. It can reduce unnecessary reads through targeted navigation.

## Kit reports

~~~powershell
.\scripts\doctor.ps1
.\scripts\doctor.ps1 -Json
.\scripts\stats.ps1
.\scripts\stats.ps1 -Json
~~~

The doctor only reports program versions and hook presence. Stats reads the tools' reports, avoids fabricated metrics and does not combine incompatible counts.
