# vlaeg — Protocolo V.L.A.E.G. para Claude Code

Plugin que guia a criação de apps, sistemas, dashboards e automações que integram com serviços externos (Slack, Shopify, Google Sheets, Notion, APIs). O projeto passa por 5 fases, nesta ordem: **V**isão, **L**ink, **A**rquitetura, **E**stilo, **G**atilho. O código fica separado em 3 camadas (A.N.T.).

## Instalar

No Claude Code:

```
/plugin marketplace add wisleyaguiar/aw-build-auto
/plugin install vlaeg@aw-build-auto
```

Requisito: `python3` no PATH (usado pelo hook e pelos `tools/` dos projetos).

## Usar

- Abra o Claude Code numa pasta vazia e descreva o que quer criar. Ex.: "quero um dashboard que lê vendas de uma planilha Google e manda resumo no Slack". A skill dispara sozinha.
- Ou chame direto: `/vlaeg:piloto`.
- Em um projeto já começado, `/vlaeg:piloto` lê o `task_plan.md` e retoma da fase atual.

## O que o plugin faz

| Peça | Função |
| --- | --- |
| Skill `piloto` | Conduz as fases V → L → A → E → G e o Loop de Reparo |
| Templates | Criam `CLAUDE.md` (Constituição), `task_plan.md`, `findings.md`, `progress.md`, `.env.example`, `.gitignore` |
| Hook `SessionStart` | Uma linha de contexto que lembra o Claude de usar a skill. Sem ela, outras instruções globais venciam e a skill não disparava sozinha |
| Hook `gate_tools.py` | Bloqueia escrita em `tools/` até os 3 portões do `task_plan.md` estarem marcados |

- No Protocolo 0 a skill copia os templates com `cp` (para não resumir nada). O Claude Code pede sua aprovação para esse comando.
- O portão é trava de processo, não de segurança: não vê escrita via Bash.

## Testar o plugin

```
python3 -m unittest hooks/test_gate_tools.py
claude plugin validate . --profile directory
```

O CI roda esses dois comandos a cada push na `main` e em cada PR.

## Lançar versão

1. Mude `version` em `.claude-plugin/plugin.json` (ex.: `0.2.0`) e faça commit na `main`.
2. `git tag v0.2.0 && git push origin v0.2.0`
3. O workflow `Release` confere se a tag bate com o `plugin.json` e cria a Release com notas automáticas.

Quem já instalou recebe o código da `main` ao atualizar o marketplace. A Release serve de marco e changelog.

## Licença

MIT. Veja [LICENSE](LICENSE).
