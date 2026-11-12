# Compatibility matrix

[Português](../pt-BR/compatibility.md) | [Home](../../README.en.md)

Hook setup can be global for a user account, but each agent exposes a different API. A GUI frontend does not necessarily forward all CLI hooks.

| Environment | Integration | Status |
| --- | --- | --- |
| Claude Code | `UserPromptSubmit` / `Stop`, last transcript usage | Testable implementation; live validation pending |
| Codex App/CLI | `PostModelRequest` / `UserPromptSubmit` | Implemented; end-to-end validation pending |
| Gemini CLI | `AfterModel` / `BeforeAgent` | Experimental opt-in |
| OpenCode | Manual `resume`, possible future plugin | No automatic hook in this version |
| Antigravity IDE | Manual `resume` | No proven automatic adapter |
| T3 Code | Depends on underlying harness | Verify per frontend |
| Orca | Manual `resume`; potential future CLI integration | No automation in this version |

Do not claim full feature parity without testing each frontend.

## Usage sources and boundaries

- **Claude:** sums `input_tokens`, `cache_read_input_tokens` and `cache_creation_input_tokens` from the latest assistant usage record, not entire session spend. JSONL may change.
- **Codex:** reads `token_usage.input_tokens` per model call when present and does not double-count cached input.
- **Gemini:** prefers `promptTokenCount`; falls back to clearly labeled `totalTokenCount` estimate. Chunked events may add overhead.
- **Unavailable counters:** no invented values or threshold notifications.
- **Smaller model windows:** set `CONTEXT_GUARD_MODEL_WINDOW` or configure lower thresholds.

The installer appends its own event groups and preserves existing hooks. Removal targets its own entries. Always preview before `-Apply`.

References: [Claude](https://docs.anthropic.com/en/docs/claude-code/hooks), [Codex](https://learn.chatgpt.com/docs/hooks), [Gemini](https://geminicli.com/docs/hooks/reference/).
