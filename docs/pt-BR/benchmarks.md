# Benchmarks e metodologia

[English](../en/benchmarks.md) | [Início](../../README.md)

Snapshot **observado localmente em 12/11/2026**, retirado dos comandos oficiais de estatísticas dos utilitários. Não é um experimento controlado de custo, qualidade ou produtividade.

| Ferramenta | Janela medida | Indicador | Valor observado |
| --- | --- | --- | --- |
| RTK 1.1.0 | Histórico global disponível | Comandos | 2.413 |
| RTK 1.1.0 | Histórico global disponível | Tokens removidos | Aproximadamente 585,1 mil |
| RTK 1.1.0 | Histórico global disponível | Redução de saída medida | 43,0% |
| Headroom 0.42.0 | Últimos 30 dias | Tokens removidos | 1.001.672 |
| Headroom 0.42.0 | Últimos 30 dias | Proporção do input total | 0,9% |
| Headroom 0.42.0 | Últimos 30 dias | Proporção do input novo | 7,1% |

**Não some as duas economias.** As ferramentas medem etapas diferentes e uma saída processada pelo RTK pode passar novamente pelo Headroom.

## Como reproduzir a leitura

~~~powershell
rtk gain
headroom savings
.\scripts\stats.ps1
.\scripts\stats.ps1 -Json
~~~

Para novos benchmarks, registre data, versões, modelo, tarefa, agente, ferramentas ativas e metodologia; compare com/sem um recurso por vez; relate tokens de entrada, cache e saída, latência e retrabalho. Separe economia estimada de medida.

Esses números não demonstram redução equivalente na **cota da assinatura** nem custo financeiro evitado.
