# Agent Optimization Kit

**Português (BR)** | [English](README.en.md)

Um setup pessoal, aberto e reproduzível para **usar melhor agentes de programação**. Este repositório documenta ferramentas, hooks, comandos, diagnósticos e medições reais, com uma camada leve de continuidade chamada **Context Guard**.

**Não é** um agente novo, um dashboard, um proxy adicional ou uma promessa de aumentar os limites dos planos.

## O que tem aqui

| Recurso | Finalidade | Estado |
| --- | --- | --- |
| [RTK](https://github.com/rtk-ai/rtk) | Reduz saída de comandos de terminal | Em uso no setup original |
| [Headroom](https://github.com/headroomlabs-ai/headroom) | Otimização de contexto por proxy | Em uso com Codex no setup original |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Grafo e busca estrutural de código | Em uso no setup original |
| **Context Guard** | Checkpoint aos 350k e preparação de handoff aos 400k | Implementação inicial, opt-in |
| **Doctor / Stats** | Diagnóstico e economia no terminal | Scripts locais |

O Context Guard **não reseta a cota de 5 horas**. Ele produz um checkpoint quando encontra dados confiáveis de contexto e ajuda a retomar o desenvolvimento em outra sessão. O checkpoint precisa ser completado pelo agente: o script não inventa decisões nem tarefas concluídas.

## Comece pelo terminal (Windows)

Requisitos: **PowerShell 5.1+**, **Python 3.10+** e **Git**. RTK, Headroom e Graphify são opcionais para os diagnósticos.

~~~powershell
cd "$HOME\Desktop\agent-optimization-kit"
.\scripts\doctor.ps1
.\scripts\stats.ps1
.\scripts\stats.ps1 -Json
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 350000
py -3 -m unittest discover -s tests -v
~~~

Instalação de hooks (primeiro **prévia**, sem mudanças):

~~~powershell
.\scripts\install-context-guard.ps1
# Apenas depois de revisar a prévia:
.\scripts\install-context-guard.ps1 -Apply
# Gemini CLI é opcional e ainda precisa de validação real:
.\scripts\install-context-guard.ps1 -Agent Gemini
~~~

Por padrão o instalador prepara **Claude Code e Codex**. Os hooks atuais não foram alterados na criação deste repositório. [Guia completo](docs/pt-BR/installation.md).

## Context Guard, em uma frase

**350.000 tokens:** prepara um checkpoint e solicita que o agente documente decisões, trabalho verificado e próximo passo.

**400.000 tokens:** sinaliza o handoff e recomenda uma sessão limpa após validar o checkpoint.

Os valores são configuráveis. Para modelos com janela menor, o script aplica limites proporcionais quando a janela é informada. Não encerra sessões, não mata processos, não aumenta permissões e não faz chamadas a APIs. [Detalhes e limites](docs/pt-BR/context-guard.md).

## Meu setup observado (12/11/2026)

| Ferramenta | Versão observada |
| --- | --- |
| RTK | 1.1.0 |
| Headroom | 0.42.0 |
| Graphify | 0.9.102 |
| Claude Code | 2.1.322 |
| Codex CLI | 0.167.2 |
| Gemini CLI | 0.68.0 |
| OpenCode | 2.2.7 |

**RTK:** 2.413 comandos analisados; aproximadamente **585,1 mil tokens filtrados (43,0%)** desde o início do histórico consultado.

**Headroom:** **1.001.672 tokens filtrados nos últimos 30 dias**, equivalentes a **7,1% do input novo** registrado pelo utilitário, e não a 7,1% da cota do plano.

As métricas usam **bases e períodos diferentes**. Não são somáveis; são relatos das ferramentas, não experimentos controlados com resultado garantido. Consulte [metodologia e histórico](docs/pt-BR/benchmarks.md).

## Documentação

- [Instalação e remoção](docs/pt-BR/installation.md)
- [Ferramentas e comandos](docs/pt-BR/tools.md)
- [Compatibilidade entre agentes e aplicativos](docs/pt-BR/compatibility.md)
- [Context Guard: funcionamento, privacidade e segurança](docs/pt-BR/context-guard.md)
- [Benchmarks e metodologia](docs/pt-BR/benchmarks.md)
- [English documentation](docs/en/installation.md)

## Privacidade e contribuições

Este repositório inclui **exemplos e implementações próprias**, não backups das configurações pessoais. Nunca publique tokens, arquivos de autenticação, transcripts, sessões ou checkpoints contendo dados privados. Os checkpoints ficam fora do repositório, no armazenamento local do usuário.

Código sob licença [MIT](LICENSE). Ferramentas de terceiros mantêm suas respectivas licenças. Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e [SECURITY.md](SECURITY.md).

**Estado atual:** kit inicial testável; integrações reais devem ser habilitadas e validadas individualmente. Nenhum ganho de quota ou compatibilidade universal é garantido.
