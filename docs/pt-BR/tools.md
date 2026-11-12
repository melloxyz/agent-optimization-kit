# Ferramentas e comandos

[English](../en/tools.md) | [Início](../../README.md)

O kit registra o setup real sem redistribuir binários de terceiros. Confira sempre a licença e o guia oficial de cada projeto.

## RTK

Projeto: https://github.com/rtk-ai/rtk

Reduz saídas de comandos antes que o agente as processe. No setup original, `rtk gain` mostrou ganhos em `rg`, ESLint, Vitest e outros comandos.

~~~powershell
rtk --version
rtk gain
rtk --help
~~~

WinGet: `winget install rtk-ai.rtk`. Leia a documentação antes de utilizar `rtk init` para não duplicar hooks.

## Headroom

Projeto: https://github.com/headroomlabs-ai/headroom

Pode otimizar contexto através de proxy local e oferece métricas próprias. No ambiente observado, o Headroom estava roteado para o **Codex**, não para Claude Code.

~~~powershell
headroom --version
headroom doctor
headroom savings
~~~

Instalado não significa roteado. Verifique com `headroom doctor`. Não sobreponha proxies sem medir cache, compatibilidade e efeito real.

## Graphify

Projeto: https://github.com/Graphify-Labs/graphify

Grafo de conhecimento e navegação estrutural do código. Foi observado um grafo no projeto DCR TUI; não há evidência de indexação de todos os projetos.

~~~powershell
graphify --version
graphify --help
~~~

Graphify não é um compressor direto de tokens: o ganho potencial vem de leituras mais seletivas.

## Scripts do kit

~~~powershell
.\scripts\doctor.ps1
.\scripts\doctor.ps1 -Json
.\scripts\stats.ps1
.\scripts\stats.ps1 -Json
~~~

O diagnóstico identifica versões e presença de hooks sem imprimir valores sensíveis. As estatísticas consultam os utilitários instalados, não estimam dados ausentes nem somam medidas incompatíveis.
