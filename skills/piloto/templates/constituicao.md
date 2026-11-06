# Constituição do Projeto (V.L.A.E.G.)

> Este arquivo é a lei. Só muda quando um esquema muda, uma regra entra ou a arquitetura muda.
> Os arquivos de planejamento (`task_plan.md`, `findings.md`, `progress.md`) são a memória.

## Estrela Guia

_O resultado único desejado._

## Regras Comportamentais

_Como o sistema deve agir: tom de voz, restrições lógicas, o que não fazer._

## Esquema de Dados

### Entrada (dados brutos)

```json
{}
```

### Saída (Payload)

```json
{}
```

## Invariantes Arquiteturais (A.N.T.)

1. **Arquitetura (`architecture/`):** POPs em Markdown. Se a lógica mudar, atualize o POP antes do código.
2. **Navegação:** o Claude roteia os dados entre POPs e tools, na ordem do Blueprint. Não faz à mão o que uma tool deve fazer.
3. **Ferramentas (`tools/`):** scripts Python determinísticos, atômicos e testáveis.

- Segredos só no `.env`. Nunca no código, nunca impressos.
- Arquivos intermediários só em `.tmp/` (podem ser apagados).
- Projeto só está concluído quando o payload chega no destino final na nuvem.

## Log de Manutenção

| Data | Mudança | Motivo |
| --- | --- | --- |
