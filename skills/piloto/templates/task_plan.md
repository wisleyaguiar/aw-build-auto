# Plano de Tarefas

> Memória do projeto: fases, objetivos e checklists. Atualize a cada avanço.

## Portões (Protocolo 0)

Nada é escrito em `tools/` até os 3 portões estarem marcados. Marque cada um só depois do OK explícito do usuário.

- [ ] Descoberta respondida
- [ ] Esquema de Dados confirmado no CLAUDE.md
- [ ] Blueprint aprovado

## Blueprint

_Preenchido na Fase V. Fluxo: entrada → etapas (POP + tool) → saída → destino._

## Fases

### V — Visão
- [ ] 5 perguntas de descoberta respondidas (`findings.md`)
- [ ] JSON Schema de entrada/saída no `CLAUDE.md`
- [ ] Pesquisa de repositórios e recursos (`findings.md`)

### L — Link
- [ ] `.env` preenchido pelo usuário
- [ ] Handshake OK para cada serviço (`tools/handshake_<servico>.py`)

### A — Arquitetura
- [ ] POP em `architecture/` + tool em `tools/` para cada etapa do Blueprint

### E — Estilo
- [ ] Payload formatado para entrega profissional
- [ ] Feedback do usuário recebido

### G — Gatilho
- [ ] Destino de produção confirmado pelo usuário
- [ ] Gatilho configurado (Cron, Webhook ou Listener)
- [ ] Payload entregue no destino final
- [ ] Log de Manutenção fechado no `CLAUDE.md`
