# Instalação e remoção

[English](../en/installation.md) | [Início](../../README.md)

## Requisitos

Windows com PowerShell 5.1+, Python 3.10+ (launcher `py -3`) e Git. RTK, Headroom e Graphify são opcionais para os diagnósticos.

~~~powershell
.\scripts\doctor.ps1
.\scripts\stats.ps1
~~~

Não há servidor, conta ou instalador npm.

## Instalar globalmente

O instalador preserva eventos existentes do perfil do usuário. Por padrão, faz apenas a **prévia** para Claude Code e Codex.

~~~powershell
.\scripts\install-context-guard.ps1
.\scripts\install-context-guard.ps1 -Agent Claude,Codex
# Apenas após revisar a prévia:
.\scripts\install-context-guard.ps1 -Apply
~~~

Gemini CLI é experimental e opt-in:

~~~powershell
.\scripts\install-context-guard.ps1 -Agent Gemini
.\scripts\install-context-guard.ps1 -Agent Gemini -Apply
~~~

`AfterModel` pode ser acionado por chunk durante streaming, causando sobrecarga de inicialização de Python. Meça antes de manter esse adaptador ativo.

Arquivos gerenciados: `~/.claude/settings.json`, `~/.codex/hooks.json` e `~/.gemini/settings.json`. Cada alteração faz backup local do JSON anterior. O instalador não altera RTK, Headroom, Graphify nem configurações de autenticação.

## Remover os hooks do kit

~~~powershell
.\scripts\install-context-guard.ps1 -Remove
.\scripts\install-context-guard.ps1 -Remove -Apply
.\scripts\install-context-guard.ps1 -Agent Gemini -Remove -Apply
~~~

Se mudar a pasta do repositório, remova os hooks e instale novamente, pois o comando registra o caminho absoluto do script.

## Testar antes

~~~powershell
py -3 -m unittest discover -s tests -v
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 349999
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 350000
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 400000
~~~

É possível validar o instalador em um perfil descartável usando `-ConfigRoot`. Não use suas configurações pessoais como fixtures.

## Retomar uma sessão

Dentro do diretório do projeto de desenvolvimento:

~~~powershell
py -3 "C:\caminho\agent-optimization-kit\hooks\context-guard\context_guard.py" status
py -3 "C:\caminho\agent-optimization-kit\hooks\context-guard\context_guard.py" resume
~~~

Copie a instrução de `resume` para o agente da próxima sessão. Não há abertura automática nem permissões ampliadas. Veja [compatibilidade](compatibility.md).
