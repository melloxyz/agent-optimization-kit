# Context Guard

[English](../en/context-guard.md) | [Início](../../README.md)

Camada local de checkpoint e retomada. Não comprime diretamente mensagens nem reinicia cotas de plano.

## Comportamento

- **350.000 tokens:** gera um `STATUS.md` local com dados Git e campos para o agente preencher, enviando aviso uma vez por nível/sessão.
- **400.000 tokens:** sinaliza handoff e recomenda sessão limpa após validar o checkpoint. Não encerra processos, não eleva permissões nem inicia outros agentes.
- **Retomada:** comandos `status` e `resume` mostram o checkpoint e a instrução para continuar.
- **Fail-open:** falta de dados, erros e formatos desconhecidos não bloqueiam o agente.

Para janelas menores, ajuste `CONTEXT_GUARD_MODEL_WINDOW`. Abaixo de 400k, warning e handoff ficam limitados a 75% e 90% da janela declarada, respectivamente.

## Variáveis

| Nome | Padrão | Descrição |
| --- | --- | --- |
| `CONTEXT_GUARD_WARNING` | 350000 | Limite de aviso |
| `CONTEXT_GUARD_HANDOFF` | 400000 | Limite de handoff |
| `CONTEXT_GUARD_MODEL_WINDOW` | Não definido | Janela para limites proporcionais |
| `AGENT_KIT_HOME` | Diretório local de dados | Local de estados e checkpoints |
| `CONTEXT_GUARD_DEBUG` | 0 | Diagnósticos opcionais |

~~~powershell
$env:CONTEXT_GUARD_MODEL_WINDOW = '200000'
py -3 .\hooks\context-guard\context_guard.py simulate --tokens 180000 --window 200000
~~~

## Privacidade

No Windows os arquivos ficam normalmente em `%LOCALAPPDATA%\agent-optimization-kit\context-guard\...`, em subpastas derivadas de hashes de projeto e sessão. O script não copia transcripts, mensagens nem respostas de ferramentas. O checkpoint registra caminho do projeto e informações do Git, que também podem ser privadas. **Nunca publique checkpoints reais.**

O checkpoint inicial contém placeholders: o agente precisa completar objetivo, decisões, evidências, testes e próximo passo. Sem validação, não se pode confiar em uma alegação de trabalho concluído.

## Limitações

A contagem é uma observação de contexto da última resposta/chamada, **não consumo cumulativo da assinatura**. Formatos de hooks e contadores variam por versão. No Codex a integração usa `PostModelRequest`, não parsing do transcript; no Gemini o contador pode ser uma estimativa.

Não há handoff automático, bloqueio rígido de ferramentas, supressão de histórico nem reinício de sessão. Teste primeiro com fixtures e em projeto descartável antes de habilitar globalmente.
