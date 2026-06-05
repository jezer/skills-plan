# Revisao de coerencia - Plano 000133 (skills no banco via API all_IA)

- Plano: 000133-skills-no-banco-postgresql-como-fonte-primaria-via-api-all-ia
- Chamado: SKILLS-JZ-CH-2026-00011
- Gerado em: 2026-06-04
- Atualizado em: 2026-06-05
- Estado: rodada 1 DECIDIDA em 2026-06-05 - 5 casos respondidos (todos opcao A). Plano executado conforme as decisoes.

## Base comparada (tudo que ja existe, varrido em 2026-06-04)

1. BANCO: modelos `SkillRegistry`/`SkillVersion`/`SkillTrigger`/... e
   router `skills.py` ja existem; `POST /skills/sync` copia disco ->
   banco com hash; `POST /skills/distribute` existe.
2. FONTE HOJE: disco (`C:\codes\skills\{core,domains,...}`); indices em
   `skills/indices` e `skills.json` mantidos por scripts ps1.
3. SINCRONIZACAO HOJE: `sincronizar-skills-ia.ps1 -Apply` (manual, no
   fechamento da manutencao); sem registro persistente de ultima sync.
4. ROTEADOR HOJE: `route-skills-by-context` le arquivos locais; nao
   consulta API nem confere frescor dos dist/.
5. DIRECAO DO WORKSPACE: o 000134 (em revisao, mesmo dia) inverte
   planos/chamados/incoerencias para banco-primario - este plano segue
   a mesma direcao para skills, eliminando o conflito original com o
   caso 4-A do 000129.

## Como decidir

1. Marque `[x]` na opcao escolhida de cada caso (uma por caso) - ou
   responda pela tela `/dev/ui > Incoerencias`.
2. Se nenhuma opcao servir, descreva a sua na linha `Outra opcao`.
3. Opcionalmente preencha `Decisao do dono:` com observacoes/condicoes.

---

## Casos da rodada 1

### Caso 1 - Fonte da verdade: autoria no disco x banco fonte unica

- Atividades: SK-05, SK-07, SK-08
- Contexto: skills sao editadas no disco (Git do repositorio skills).
  O banco pode ser fonte primaria de DISTRIBUICAO e CONSULTA (autoria
  continua no disco e publica no banco) ou fonte UNICA inclusive de
  autoria (editar skill = editar no banco).
- Impacto: define onde vive o conteudo oficial e o papel do Git.

Opcoes:

- [x] A) AUTORIA NO DISCO + BANCO PRIMARIO DE DISTRIBUICAO/CONSULTA: quem edita skill edita no disco (Git preservado como historico de autoria); `finalizar-manutencao-skills.ps1` PUBLICA no banco (hash + alterado_em); dist/ e indice sao gerados DO BANCO; consulta da CLI sempre via API. (Recomendada - Git continua valendo, banco manda na distribuicao)
- [ ] B) BANCO FONTE UNICA: autoria tambem no banco (editor/API), disco vira espelho gerado inclusive em C:\codes\skills - rompe o fluxo Git atual de autoria, mudanca bem maior.
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 2 - Granularidade da sincronizacao banco -> dist/

- Atividades: SK-07
- Contexto: quando o roteador detectar defasagem, sincronizar tudo ou
  somente as skills com `alterado_em > ultima_sync`?
- Impacto: latencia do prompt quando houver sync automatica.

Opcoes:

- [x] A) DELTA POR HASH: somente skills alteradas apos a ultima sync do destino (comparacao por hash/alterado_em); comando manual continua podendo forcar sync total. (Recomendada - sync rapida no meio do prompt)
- [ ] B) SYNC TOTAL a cada defasagem (mais simples, mais lenta, regrava tudo).
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 3 - Check de frescor no inicio do prompt

- Atividades: SK-09
- Contexto: o roteador consulta `GET /skills/sync/status` a cada inicio
  de prompt. Backend local responde em ms, mas se estiver fora, o check
  nao pode travar o prompt.
- Impacto: latencia e robustez de TODO inicio de sessao.

Opcoes:

- [x] A) CHAMADA DIRETA COM TIMEOUT CURTO: uma chamada HTTP local por prompt (timeout ~500ms); falhou/timeout = fallback offline (usa dist/ local como esta e registra pendencia de sync); sem cache. (Recomendada - estado sempre fresco, custo minimo local)
- [ ] B) CACHE LOCAL COM TTL: resultado do status cacheado por N minutos; reduz chamadas, pode rotear com dist/ defasado dentro da janela do TTL.
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 4 - Escopo do conteudo da skill no banco

- Atividades: SK-05, SK-07
- Contexto: para o dist/ ser GERADO do banco, o banco precisa ter tudo
  que a skill distribui. Skills tem SKILL.md + scripts + templates +
  assets + referencias.
- Impacto: se o banco tiver so o SKILL.md, o dist/ nao pode ser gerado
  100% do banco e a fonte primaria fica pela metade.

Opcoes:

- [x] A) PACOTE COMPLETO: todos os arquivos da skill no banco (conteudo + hash por arquivo); dist/ regeneravel inteiramente do banco; payload da API de consulta continua enxuto (conteudo completo so em GET /skills/{nome}). (Recomendada - coerente com banco fonte primaria de distribuicao)
- [ ] B) SOMENTE SKILL.md + frontmatter no banco; scripts/assets continuam copiados do disco na sync (banco primario parcial - indice e conteudo principal no banco, anexos no disco).
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 5 - Governanca: o que executa no contexto all_IA x skills

- Atividades: SK-04, SK-05, SK-06
- Contexto: modelo de dados e API sao do contexto tools/all_IA; roteador,
  sincronizador e maintain-skills sao do contexto skills. Mesmo padrao do
  caso 8-A do 000130 e caso 8 do 000134.
- Impacto: rastreabilidade da mudanca entre contextos.

Opcoes:

- [x] A) ALTERACAO DIRETA AMPARADA + PEDIDO ESPELHADO FORMAL: SK-04 registra o pedido espelhado no plan do tools/all_IA (rastreabilidade), mas a execucao de SK-05/SK-06 segue direto neste fluxo citando o pedido explicito do dono (esta conversa) no commit e na sessao do chamado - sem aguardar ciclo separado. (Recomendada - mesmo precedente do 000130/000134)
- [ ] B) Pedido espelhado e execucao SOMENTE pelo contexto all_IA em plano proprio dele (mais formal, mais lento, dois planos para uma feature).
- [ ] Outra opcao (descrever):

Decisao do dono:

---

## Proximos passos apos decisao

1. Dono marca `[x]` em cada caso (ou descreve outra opcao) e preenche
   `Decisao do dono:` quando quiser detalhar.
2. SK-03 fecha; execucao segue SK-04..SK-99 conforme as escolhas.
3. Registrar a rodada na sessao do chamado SKILLS-JZ-CH-2026-00011 e
   atualizar o campo `Estado:` deste arquivo.
