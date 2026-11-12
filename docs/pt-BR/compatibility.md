# Compatibilidade

[English](../en/compatibility.md) | [Início](../../README.md)

O registro dos hooks é global por perfil de usuário, mas cada agente tem sua própria API. Um frontend não necessariamente expõe todas as capacidades da CLI.

| Ambiente | Integração | Situação |
| --- | --- | --- |
| Claude Code | `UserPromptSubmit` + `Stop`, uso no transcript | Código e fixtures testáveis; validar sessão real |
| Codex App/CLI | `PostModelRequest` + `UserPromptSubmit` | Implementado; validação end-to-end pendente |
| Gemini CLI | `AfterModel` + `BeforeAgent` | Experimental e opcional |
| OpenCode | `resume` manual; plugin possível no futuro | Sem hook automático |
| Antigravity IDE | `resume` manual | Sem integração automática comprovada |
| T3 Code | Depende do harness executado | Teste por frontend |
| Orca | `resume` manual, CLI opcional no futuro | Sem automação nesta versão |

Não anuncie paridade entre ambientes sem testes reais.

## Medição e limites

- **Claude:** soma `input_tokens`, `cache_read_input_tokens` e `cache_creation_input_tokens` da última resposta observada. O formato JSONL pode mudar.
- **Codex:** usa `token_usage.input_tokens` por requisição, sem adicionar novamente tokens em cache.
- **Gemini:** prefere `promptTokenCount`; se só houver `totalTokenCount`, sinaliza como estimativa. Eventos podem ser disparados por chunk.
- **Sem contagem:** não dispara checkpoints nem inventa valores.
- **Modelos com janela menor:** configure `CONTEXT_GUARD_MODEL_WINDOW`; os padrões de 350k/400k não servem para qualquer modelo.

## Hooks existentes

O instalador acrescenta grupos próprios sem apagar outros hooks. A remoção é direcionada às entradas do kit. Faça backup, examine a prévia e só então utilize `-Apply`.

Referências: [Claude](https://docs.anthropic.com/en/docs/claude-code/hooks), [Codex](https://learn.chatgpt.com/docs/hooks), [Gemini](https://geminicli.com/docs/hooks/reference/).
