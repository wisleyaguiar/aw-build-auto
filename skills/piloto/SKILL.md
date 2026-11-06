---
name: piloto
description: Use SEMPRE, antes de escrever qualquer código, quando o usuário pedir para criar um aplicativo, sistema, dashboard, automação, bot, relatório automático ou integração que conecta serviços externos (Slack, Shopify, Google Sheets, Notion, e-mail, CRMs, APIs, webhooks). Ex.: "quero um dashboard que lê vendas da planilha e manda resumo no Slack". Conduz o projeto pelo protocolo V.L.A.E.G. (Visão, Link, Arquitetura, Estilo, Gatilho) e impede código antes da descoberta, do esquema de dados e do blueprint aprovados.
---

# Piloto do Sistema — Protocolo V.L.A.E.G.

Você conduz o projeto como **Piloto**. Siga as fases **V.L.A.E.G.** (Visão, Link, Arquitetura, Estilo, Gatilho) e separe o código nas 3 camadas **A.N.T.** O objetivo é uma automação que dá sempre o mesmo resultado e se conserta quando quebra. Prefira o certo ao rápido. Regra de negócio que não está clara vira pergunta ao usuário, nunca suposição.

## 1. Roteador de estado (sempre primeiro)

Olhe a raiz do projeto (pasta atual):

- **Sem `task_plan.md`** → rode o Protocolo 0.
- **Com `task_plan.md`** → leia `## Portões (Protocolo 0)` e `## Fases`. Diga ao usuário em que fase o projeto está (primeiro item não marcado) e retome dali. Leia também `progress.md` para saber do último erro ou passo.

## 2. Protocolo 0 — Inicialização (obrigatório)

Antes de qualquer código, copie os templates para a raiz do projeto (pasta atual). Faça isso logo, sem pedir licença: é o primeiro passo do protocolo e só cria arquivos de planejamento. Rode este bloco no Bash, trocando `<pasta base desta skill>` pelo caminho que o Claude Code informou ao carregar a skill:

```bash
T="<pasta base desta skill>/templates"
cp -n "$T/task_plan.md" "$T/findings.md" "$T/progress.md" .
cp -n "$T/env.example" .env.example
echo >> CLAUDE.md; cat "$T/constituicao.md" >> CLAUDE.md
echo >> .gitignore; cat "$T/gitignore" >> .gitignore
```

- **Não reescreva nem resuma os templates.** Copie como estão; preencha as seções durante as fases.
- `CLAUDE.md` e `.gitignore` recebem o template no fim (anexar). Nunca sobrescreva o que já existe.
- `CLAUDE.md` é a Constituição: esquemas de dados, regras comportamentais, invariantes arquiteturais.
- **Proibido escrever em `tools/`** até estes 3 portões estarem marcados no `task_plan.md`:
  - `- [x] Descoberta respondida`
  - `- [x] Esquema de Dados confirmado no CLAUDE.md`
  - `- [x] Blueprint aprovado`
- Um hook do plugin bloqueia escrita em `tools/` enquanto faltar algum portão. Se ele bloquear, termine o portão. Não contorne via Bash.
- **Marque cada portão só depois do OK explícito do usuário.** Nunca marque por conta própria.

## 3. Fase V — Visão (e Lógica)

1. **Descoberta:** faça as 5 perguntas numa mensagem só (são abertas, responda em texto):
   - **Estrela Guia:** qual é o resultado único desejado?
   - **Integrações:** quais serviços externos são necessários? As chaves estão prontas?
   - **Fonte da Verdade:** onde vivem os dados primários?
   - **Payload de Entrega:** como e onde o resultado final deve ser entregue?
   - **Regras Comportamentais:** como o sistema deve agir? (tom de voz, restrições lógicas, o que não fazer)

   Grave as respostas em `findings.md`. Resposta vaga? Pergunte de novo. Ao fim, peça OK e marque `Descoberta respondida`.
2. **Dados Primeiro:** escreva no `CLAUDE.md` o JSON Schema de entrada (dados brutos) e de saída (Payload), mais Estrela Guia e Regras Comportamentais. Mostre ao usuário. Com o OK, marque `Esquema de Dados confirmado no CLAUDE.md`.
3. **Pesquisa:** procure repositórios, bibliotecas e docs de API úteis (`gh search repos <termos> --limit 10`, WebSearch, Context7). Use subagentes para pesquisas em paralelo. Registre o que serve em `findings.md`.
4. **Blueprint:** preencha `## Blueprint` no `task_plan.md`: entrada → etapas (um POP + uma tool por etapa) → saída → destino. Com o OK, marque `Blueprint aprovado`.

## 4. Fase L — Link (Conectividade)

1. Peça ao usuário para criar `.env` a partir de `.env.example` e preencher as chaves. **Nunca leia nem mostre valores do `.env` no chat.**
2. **Handshake:** para cada serviço, copie `templates/handshake.py` para `tools/handshake_<servico>.py` e ajuste `SERVICE`, `REQUIRED` e `URL` (ou troque pelo SDK oficial).
3. Rode `python3 tools/handshake_<servico>.py`. Saída esperada: `OK <servico>`.
4. **Não siga para a lógica completa com algum Link quebrado.** Falhou? Use o Loop de Reparo.

## 5. Fase A — Arquitetura (3 camadas A.N.T.)

LLMs são probabilísticos. A lógica de negócio deve ser determinística.

- **Camada 1 — Arquitetura (`architecture/`):** antes de cada tool, crie o POP a partir de `templates/pop.md` (objetivo, entradas e saída, lógica, casos de borda). **Regra de Ouro:** se a lógica mudar, atualize o POP antes do código.
- **Camada 2 — Navegação (você):** roteie os dados entre POPs e tools, na ordem do Blueprint. Não faça à mão o que uma tool deve fazer.
- **Camada 3 — Ferramentas (`tools/`):** scripts Python determinísticos e atômicos. Cada um roda sozinho, recebe e devolve JSON, e sai com código ≠ 0 em erro. Lógica não trivial ganha teste em `tools/tests/` (unittest). Segredos só do `.env`. Arquivos intermediários só em `.tmp/`.

## 6. Fase E — Estilo (Refinamento e UI)

1. **Payload:** formate a saída para entrega profissional (blocos do Slack, layout do Notion, HTML de e-mail).
2. **UI/UX:** dashboard ou frontend com HTML/CSS limpo e layout intuitivo.
3. **Feedback:** mostre o resultado ao usuário e ajuste antes do deploy.

## 7. Fase G — Gatilho (Implantação)

1. **Confirme com o usuário** o destino de produção e o que será publicado. Deploy é ação externa: nada sobe sem OK.
2. **Nuvem:** mova a lógica testada do ambiente local para produção.
3. **Automação:** configure o gatilho (Cron, Webhook ou Listener).
4. **Documentação:** feche o Log de Manutenção no `CLAUDE.md`.
5. O projeto só está **concluído** quando o payload chega ao destino final na nuvem.

## 8. Princípios Operacionais

**Dados Primeiro.** Nenhuma tool antes do Esquema de Dados no `CLAUDE.md`. Código só depois do formato do Payload confirmado.

**Depois de cada tarefa significativa:**
- `progress.md`: o que foi feito, erros, testes, resultados.
- `findings.md`: descobertas e restrições.
- `CLAUDE.md`: só quando um esquema muda, uma regra entra ou a arquitetura muda.
- `CLAUDE.md` é a lei. Os arquivos de planejamento são a memória.

**Loop de Reparo** (quando uma tool falha):
1. **Analisar:** leia o stack trace e a mensagem de erro. Não adivinhe.
2. **Corrigir:** ajuste o script em `tools/`.
3. **Testar:** confirme que a correção funciona.
4. **Atualizar Arquitetura:** registre o aprendizado no POP em `architecture/` (ex.: "a API exige o header X", "limite de 5 chamadas/seg") para o erro não se repetir.

**Entregáveis vs. Intermediários:**
- Local (`.tmp/`): dados coletados, logs, temporários. Efêmeros.
- Global (nuvem): o Payload (Google Sheets, banco de dados, UI). É ele que define "concluído".

## Estrutura do projeto gerado

```
├── CLAUDE.md          # Constituição: schemas, regras, invariantes, log
├── task_plan.md       # Portões, Blueprint, fases
├── findings.md        # Descobertas e pesquisa
├── progress.md        # O que foi feito e erros
├── .env               # Chaves (verificadas na fase Link; nunca no git)
├── architecture/      # Camada 1: POPs
├── tools/             # Camada 3: scripts Python
└── .tmp/              # Intermediários
```

| Passo | Pergunta-chave | Quando |
| --- | --- | --- |
| **V** Visão | O que entra e o que sai? | Antes de tudo |
| **L** Link | Os fios estão conectados? | Antes do código |
| **A** Arquitetura | Quem faz o quê? | Durante a construção |
| **E** Estilo | Está bonito para o cliente? | Depois que funciona |
| **G** Gatilho | Roda sozinho? | No final (deploy) |
