<!-- GERADO DO BANCO (000134) - nao editar manualmente; edite pela tela, API ou skill do all_IA -->
# 000133 - skills no banco postgresql como fonte primaria via api all_ia

- Numero: 000133
- Titulo: skills no banco postgresql como fonte primaria via api all_ia
- Dono: skills
- Usuario atual: jz
- Prioridade: 2
- Status: concluido
- Criado em: 2026-06-04
- Atualizado em: 2026-06-05
- Chamado: SKILLS-JZ-CH-2026-00011
- Skills relacionadas: maintain-skills, route-skills-by-context, maintain-planner, maintain-activities, fastapi-specialist, alembic-db-specialist

## Objetivo

Pedido do dono (2026-06-04): o banco PostgreSQL do all_IA passa a ser a
FONTE PRIMARIA de todas as skills do workspace, com o indice de skills de
facil acesso pelo banco. Todas as skills ficam registradas no banco
(conteudo + metadados + datas de alteracao). Ao iniciar um prompt, a skill
roteadora (`route-skills-by-context`) consulta, SEMPRE VIA API do all_IA,
se a ultima data de sincronizacao banco -> diretorios das IAs
(`dist/{claude,codex,copilot,gemini}`) e posterior a maior data de
alteracao de skill no banco; se existir skill alterada DEPOIS da ultima
sincronizacao, o sincronizador e invocado automaticamente antes de seguir.
As APIs devem usar as melhores tecnicas de indexacao e performance do
PostgreSQL para responder com baixa latencia a CLI.

## Fundamento e estado real (levantamento em 2026-06-04)

1. BANCO HOJE: all_IA usa PostgreSQL (`DATABASE_URL=postgresql://...@localhost:5432/all_ia`
   em `tools/all_IA/.env`); ja existem modelos `SkillRegistry`,
   `SkillVersion`, `SkillTrigger`, `SkillTriggerLink`, `SkillScriptLink`
   em `backend/app/models.py` e router `backend/app/routers/skills.py`
   com endpoints de listar/obter/criar skill, versions, triggers,
   scripts, tree, `POST /skills/sync` (disco -> banco com hash) e
   `POST /skills/distribute`.
2. FONTE PRIMARIA HOJE: a fonte da verdade e o DISCO
   (`C:\codes\skills\{core,domains,generators,synchronizers}`); o banco
   so recebe copia via `POST /skills/sync`. Indices auxiliares ficam em
   `skills/indices` e `skills/skills.json`, mantidos por scripts ps1
   (`atualizar-indices-skills.ps1`, `generate_skills_json.ps1`).
3. SINCRONIZACAO HOJE: `maintain-skills/scripts/sincronizar-skills-ia.ps1 -Apply`
   copia skills oficiais do disco para `dist/{claude,codex,copilot,gemini}`;
   execucao e MANUAL (fim de manutencao via
   `finalizar-manutencao-skills.ps1`). Nao existe registro persistente de
   "ultima sincronizacao" consultavel por API, nem comparacao automatica
   com a maior data de alteracao de skill.
4. ROTEADOR HOJE: `route-skills-by-context` (core/router) decide skills
   executoras por contexto lendo arquivos locais; nao consulta API nem
   verifica frescor dos `dist/` antes de rotear.
5. PRECEDENTES: o plano 000130 (tools/all_IA) ja adapta `maintain-planner`
   para consumir API de planos; o caso 4 do 000129 decidiu "workspace e a
   fonte" para PLANOS. Este plano inverte a direcao para SKILLS (banco
   como fonte primaria), o que exige decisao explicita de coerencia entre
   os dois modelos na revisao de coerencia (caso a ser registrado).
6. GOVERNANCA: mudancas na API/banco sao do contexto `tools/all_IA`;
   mudancas nas skills (`route-skills-by-context`, `maintain-skills`,
   sincronizador) sao deste contexto `skills`. Este plano e o dono da
   visao; os itens de API geram pedido/atividade espelhada no plan do
   all_IA conforme autonomia por contexto (root, secao Autonomia).

## Escopo

Inclui:

1. MODELO DE DADOS: consolidar no PostgreSQL o registro completo de
   skills - conteudo do `SKILL.md` (e arquivos auxiliares referenciados),
   metadados do frontmatter, dominio/camada, hash de conteudo,
   `alterado_em` por skill - e tabela de controle de sincronizacao
   `skill_sync_run` (destino, iniciado_em, concluido_em, status,
   hash_snapshot, qtd_skills) para registrar cada execucao do
   sincronizador banco -> diretorios das IAs.
2. INDICE NO BANCO: indice de skills consultavel por query simples
   (view/materialized view ou endpoint dedicado), substituindo a
   dependencia primaria de `skills/indices/*.json` e `skills.json`
   (que passam a ser derivados/secundarios).
3. API DE SKILLS (all_IA): endpoints de leitura rapida para a CLI -
   `GET /skills/index` (indice completo enxuto), `GET /skills/{nome}`
   (conteudo + metadados), `GET /skills/sync/status` (ultima sync por
   destino + `max(alterado_em)` das skills + flag `defasado`),
   `POST /skills/sync/run` (dispara sincronizador banco -> dist/) -
   com tecnicas de indexacao e performance do PostgreSQL: indices
   B-tree em `nome`/`alterado_em`, GIN (pg_trgm/tsvector) para busca
   textual de triggers/descricao, paginacao, ETag/If-None-Match por
   hash, payloads enxutos e query unica para o status de defasagem.
4. SINCRONIZADOR: evoluir o fluxo para banco -> `dist/{claude,codex,copilot,gemini}`
   como caminho oficial de distribuicao, registrando cada execucao em
   `skill_sync_run`; o caminho disco -> banco (`POST /skills/sync`)
   permanece como ingestao de autoria (quem edita skill no disco publica
   no banco no fechamento da manutencao via `finalizar-manutencao-skills.ps1`).
5. ROTEADOR COM CHECK DE FRESCOR: `route-skills-by-context` (e o
   `session-bootstrap.ps1`) passa a, no inicio do prompt/sessao,
   chamar `GET /skills/sync/status`; se `max(alterado_em) > ultima_sync`
   de algum destino, invocar o sincronizador (via `POST /skills/sync/run`
   ou script local) antes de rotear; em caso de API indisponivel,
   fallback offline documentado (usa `dist/` local como esta e registra
   pendencia de sync).
6. ADAPTACAO DE `maintain-skills`: fechamento de manutencao publica a
   skill alterada no banco (atualiza `alterado_em`/hash) e os indices
   derivados; validacoes existentes (quick_validate, indices) permanecem.
7. Testes (pytest no all_IA, testes ps1 das skills), documentacao e
   revisao de coerencia com decisao do dono antes da implementacao.

Nao inclui:

1. Migrar PLANOS para banco como fonte primaria (000129/000130 sao os
   donos dessa direcao).
2. Editor de skills na tela do all_IA (autoria continua no disco/Git);
   se surgir, plano proprio.
3. Mudar o conteudo/proposito das skills existentes; apenas registro,
   indice e distribuicao.
4. Multi-maquina em tempo real (jz/jf simultaneos no mesmo banco);
   registrar pendencia se necessario.

## Avaliacao de conflitos

Rodada 1 ABERTA: 5 casos aguardando decisao do dono em
`revisao-coerencia.md` (respondiveis pela tela /dev/ui > Incoerencias):
fonte da verdade (autoria disco x banco unico), granularidade de sync
(delta por hash x total), check de frescor no prompt (API direta x
cache TTL), escopo do conteudo no banco (pacote completo x so SKILL.md)
e governanca all_IA x skills.

## Atividades planejadas

| # | Atividade | Status | Skill executora | Saida |
|---|---|---|---|---|
| SK-01 | Insumos do dono (pedido desta conversa) | concluido | maintain-planner | objetivo registrado |
| SK-02 | Levantamento de estado real (banco, API, sincronizador, roteador) | concluido | maintain-planner | secao fundamento |
| SK-03 | Revisao de coerencia (casos 1-5) + decisao do dono | concluido | maintain-planner | 5 casos decididos (todos A) |
| SK-04 | Pedido espelhado no plan de tools/all_IA (modelo de dados + API) | concluido | maintain-planner | executado em conjunto com o 000134 (caso 5-A: alteracao direta amparada; rastreabilidade no chamado e nos commits) |
| SK-05 | Modelo de dados: skill completa no banco + `skill_sync_run` + indices PostgreSQL (B-tree, GIN/pg_trgm) | concluido | alembic-db-specialist | skill_file/skill_sync_run + hash_pacote/alterado_em (migration 0019); GIN pg_trgm guardado por dialeto |
| SK-06 | API de leitura performatica: `GET /skills/index`, `GET /skills/{nome}`, `GET /skills/sync/status`, `POST /skills/sync/run` (ETag, paginacao, query unica de defasagem) | concluido | fastapi-specialist | index 12ms / status 9ms local (medido); ETag/304 |
| SK-07 | Sincronizador banco -> dist/{claude,codex,copilot,gemini} com registro em `skill_sync_run` (delta por hash conforme caso 2) | concluido | maintain-skills | skill_sync.py; validado: 45 skills publicadas, 4 destinos concluidos, delta por hash |
| SK-08 | Ingestao de autoria: `finalizar-manutencao-skills.ps1` publica skill alterada no banco (hash + alterado_em) | concluido | maintain-skills | POST /skills/sync + sync/run no fechamento; pendencia offline em indices/.sync-banco-pendente |
| SK-09 | Roteador com check de frescor: `route-skills-by-context`/`session-bootstrap.ps1` consulta `sync/status` via API e dispara sync quando defasado, com fallback offline | concluido | route-skills-by-context | verificar-frescor-skills.ps1 (timeout 500ms, 127.0.0.1, sem proxy); hook no session-bootstrap |
| SK-90 | Testes (pytest all_IA + testes ps1 skills) + docs + re-levantamento banco x modelos | concluido | automated-test-builder | 296 testes verdes + ruff; validate-skills 45/45; zero orfas |
| SK-99 | Conclusao do plano e sync | concluido | maintain-planner | plano em concluido/ |

## Criterio de aceite

1. Toda skill oficial do workspace existe no banco PostgreSQL com
   conteudo, frontmatter, dominio, hash e `alterado_em`; o indice de
   skills e consultavel por uma unica chamada `GET /skills/index`.
2. `GET /skills/sync/status` responde, em uma unica query indexada, a
   ultima sincronizacao por destino, o `max(alterado_em)` das skills e a
   flag `defasado`, sem varrer disco.
3. Alterar uma skill (fechamento de manutencao) e iniciar um prompt em
   seguida faz o roteador detectar `alterado_em > ultima_sync` e invocar
   o sincronizador automaticamente; ao final, `dist/{claude,codex,copilot,gemini}`
   refletem o banco e `skill_sync_run` registra a execucao.
4. Quando nao ha skill alterada apos a ultima sync, o roteador NAO
   dispara sincronizacao e o check adiciona latencia minima ao prompt
   (uma chamada HTTP local ou cache conforme caso 3).
5. Com o backend all_IA desligado, o roteador segue funcionando em
   fallback offline (usa dist/ local) e registra pendencia de sync.
6. Os dados sao sempre consultados via API do all_IA (CLI/skills nao
   abrem conexao direta com o PostgreSQL).
7. Suite pytest + ruff do all_IA verde; quick_validate e indices das
   skills validados; docs atualizados; plano valido; re-levantamento
   banco x modelos sem colunas orfas.

## Checklist

- [x] Insumos registrados (SK-01).
- [x] Levantamento de estado real (SK-02).
- [x] Revisao de coerencia decidida pelo dono (SK-03).
- [x] Pedido espelhado no plan de tools/all_IA (SK-04).
- [x] Modelo de dados + skill_sync_run + indices PostgreSQL (SK-05).
- [x] API de leitura performatica (SK-06).
- [x] Sincronizador banco -> dist/ com registro (SK-07).
- [x] Ingestao de autoria no fechamento de manutencao (SK-08).
- [x] Roteador com check de frescor + fallback offline (SK-09).
- [x] Testes + docs + re-levantamento (SK-90).
- [x] Plano concluido e sincronizado (SK-99).

## Skills recomendadas atuais

- maintain-planner / maintain-activities: plano, revisao de coerencia,
  gates e conclusao.
- route-skills-by-context: roteamento por bloco e a propria adaptacao do
  check de frescor (SK-09).
- maintain-skills: sincronizador, ingestao de autoria e validacoes
  (SK-07, SK-08).
- fastapi-specialist: endpoints de leitura performatica (SK-06).
- alembic-db-specialist: modelo de dados e indices PostgreSQL (SK-05).
- automated-test-builder / technical-writer: testes e docs (SK-90).

## Riscos

1. Duas fontes da verdade (disco x banco) divergirem - mitigacao: caso 1
   define a direcao (autoria no disco -> publicacao no banco ->
   distribuicao do banco), com hash por skill para detectar divergencia.
2. Check de API a cada prompt criar dependencia dura do backend -
   mitigacao: fallback offline (criterio 5) + cache/TTL (caso 3).
3. Sincronizacao automatica no meio de um prompt sobrescrever dist/ em
   uso por outra sessao - mitigacao: lock existente
   (`acquire-skill-lock.ps1`) e sync delta atomica por skill.
4. Alterar API/banco do all_IA a partir do contexto skills ferir a
   autonomia por contexto - mitigacao: SK-04 registra pedido espelhado
   no plan do all_IA; o pedido explicito do dono nesta conversa ampara o
   plano conjunto.
5. Indice no banco defasar dos arquivos `skills/indices/*.json` -
   mitigacao: indices de arquivo passam a ser derivados do banco (ou
   validados contra ele) no fechamento de manutencao.
6. Performance da API degradar com crescimento do conteudo - mitigacao:
   payloads enxutos no index, conteudo completo so em `GET /skills/{nome}`,
   ETag por hash, indices B-tree/GIN e paginacao.

## Validacao planejada

1. `validar-plano.ps1` (estrutura).
2. pytest + ruff no all_IA por bloco; testes ps1 das skills
   (`run-skill-tests.ps1`); instancia de teste nas portas 8128-8139
   (nunca a 8000): alterar skill -> fechar manutencao -> iniciar prompt
   -> ver sync automatica -> conferir `skill_sync_run` e dist/.
3. Medir latencia de `GET /skills/index` e `GET /skills/sync/status`
   antes da conclusao.
4. Conclusao via `concluir-plano.ps1` + re-levantamento banco x modelos.

## Correlacao Obrigatoria de Skills

1. Roteamento registrado na sessao 014 do chamado SKILLS-JZ-CH-2026-00011:
   executora maintain-planner; apoio route-skills-by-context,
   maintain-skills, maintain-activities.
2. Reexecutar `route-skills-by-context` antes de cada bloco (SK-05 a
   SK-09) e registrar na sessao ativa.
