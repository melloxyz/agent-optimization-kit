# Contribuindo / Contributing

## Português (BR)

Obrigado por considerar uma contribuição. O objetivo é manter o kit **pequeno, reproduzível, seguro e independente de fornecedor**.

- Abra uma issue antes de propor alterações grandes.
- Não envie configurações reais, arquivos de autenticação, transcripts ou checkpoints privados.
- Ao adicionar uma ferramenta, documente o que ela faz, versão, origem oficial, configuração, limitações, comandos e método de medição.
- Atualize as versões em português e inglês da documentação.
- Rode `py -3 -m unittest discover -s tests -v` antes de enviar PR.
- Novos hooks devem ser opcionais, reversíveis, compatíveis com outros hooks e fail-open por padrão.
- Não afirme economia de cotas sem medição com metodologia comparável.

## English

Thanks for contributing. Keep this kit **small, reproducible, safe and vendor-neutral**.

- Open an issue before proposing large changes.
- Do not submit real user configurations, authentication files, transcripts or private checkpoints.
- Document each new tool's purpose, version, official source, setup, limits, commands and measurement method.
- Keep PT-BR and English documentation in sync.
- Run `py -3 -m unittest discover -s tests -v` before opening a PR.
- Hooks must be opt-in, reversible, coexist with other hooks and fail open by default.
- Do not claim quota savings without comparable measurement evidence.
