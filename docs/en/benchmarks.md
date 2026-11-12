# Benchmarks and methodology

[Português](../pt-BR/benchmarks.md) | [Home](../../README.en.md)

Reference snapshot **observed locally on 2026-11-12** using each upstream tool's own reporting command. This is not a controlled benchmark of quality, cost, or productivity.

| Tool | Reporting period | Metric | Observed value |
| --- | --- | --- | --- |
| RTK 1.1.0 | Available global lifetime | Commands | 2,413 |
| RTK 1.1.0 | Available global lifetime | Tokens removed | Roughly 585.1k |
| RTK 1.1.0 | Available global lifetime | Output reduction | 43.0% |
| Headroom 0.42.0 | Last 30 days | Tokens removed | 1,001,672 |
| Headroom 0.42.0 | Last 30 days | Share of all forwarded input | 0.9% |
| Headroom 0.42.0 | Last 30 days | Share of new input | 7.1% |

**Do not add the savings together.** They are different stages of processing, and RTK-filtered outputs may pass through Headroom.

## Reproduce locally

~~~powershell
rtk gain
headroom savings
.\scripts\stats.ps1
.\scripts\stats.ps1 -Json
~~~

For future comparisons, record the date, tool versions, model, task, agent, enabled integrations and method; compare with/without one feature at a time; report input, cache, output, latency and rework when measurable. Keep estimates distinct from measured values.

These numbers do not imply proportional gains in **subscription quota** or verified monetary savings.
