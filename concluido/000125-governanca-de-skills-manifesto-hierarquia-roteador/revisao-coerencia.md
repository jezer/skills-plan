# Revisao de coerencia - Plano 000125 (governanca de skills) x workspace skills ja implementado

- Plano: 000125-governanca-de-skills-manifesto-hierarquia-roteador
- Chamado: TOOLS-JZ-CH-2026-00123
- Gerado em: 2026-06-04
- Atualizado em: 2026-06-04
- Estado: rodada 1 DECIDIDA (7 casos, todos opcao A) e EXECUTADA em
  2026-06-04. Incoerencia extra encontrada e corrigida na execucao: o Fluxo
  da maintain-skills ainda dizia "frontmatter somente name e description"
  (contradizia triggers/manifesto oficiais).

## Rodada 1 - decisoes (todas A) aplicadas

| # | Caso | Efeito |
|---|---|---|
| 1 | Manifesto = so o NOVO em metadata (camada/escopo_negativo/dependencias/saidas) | formato oficial na maintain-skills |
| 2 | Camada declarativa, sem mover pastas | metadata.camada |
| 3 | dependencias declaradas + wikilinks (uniao no consumidor) | sync do all_IA le ambos |
| 4 | Obrigatorio em skills novas + aviso nas existentes | validate-skills.ps1 + manifesto-baseline.txt |
| 5 | Fallback duplo (roteador + frase nos Limites) | secao no router + 18 skills |
| 6 | Lote 18 (10 do 000118 + 8 ferramentas) | populadas |
| 7 | Consumo imediato no all_IA | migration 0014 + sync + tela |

## Base comparada (tudo que ja existe, varrido em 2026-06-04)

1. PADRAO DO CORPO: toda SKILL.md ja tem `## Objetivo`, `## Uso` e
   `## Limites` (regra root "toda skill declara objetivo, uso e limites").
   `## Limites` ja E um escopo negativo INFORMAL (texto livre, nao
   maquina-legivel). O manifesto proposto (proposito/escopo positivo/
   negativo) SOBREPOE essas secoes - duplicar criaria duas fontes da verdade.
2. FRONTMATTER: o validador padrao (`quick_validate.py`) so permite chaves
   extras DENTRO de `metadata` (precedente: `metadata.triggers` do 000118,
   ja populado em 10 skills e consumido pelo all_IA). Subcampos livres em
   metadata sao aceitos - `metadata.camada`, `metadata.escopo_negativo` etc.
   passam na validacao sem tocar o validador do sistema.
3. CAMADAS x ESTRUTURA FISICA: a hierarquia proposta
   (ferramenta/atividade/padroes) NAO mapeia nas pastas atuais
   (`core/<dominio>` e `domains/<dominio>`). Exemplos reais:
   `redshift-sql-specialist` (ferramenta) e `redshift-query-rules-comparator`
   (atividade/padroes) convivem em `domains/languages`;
   `postgresql-support` (ferramenta) esta em `domains/tools`. Reorganizar
   fisicamente mexe em dist/, registros do all_IA e nos 4 espelhos por IA.
4. DEPENDENCIAS: ja existe a convencao `[[wikilink]]` no corpo, consumida
   pelo all_IA (`SkillDependency` + dependentes na API/tela) - uso raro hoje
   (1 ocorrencia). O manifesto propoe `dependencias` declaradas - segundo
   mecanismo para a mesma coisa se nao for unificado.
5. ROTEADOR: `route-skills-by-context` tem Objetivo/Uso/Limites/Fluxo -
   NAO ha protocolo formal de fallback ("isto nao e meu proposito ->
   devolver ao roteador"); a regra root 24 ja diz que skill nao executa
   proposito de outra, mas nenhuma skill declara o caminho de devolucao.
6. SAIDAS PARAMETRIZADAS: a `maintain-skills` ja exige scripts
   parametrizados (`param(...)`, argparse) nas regras de Scripts - o
   principio "saida reutilizavel" ja existe; falta o campo declarado
   (`saidas`) e a priorizacao explicita de script sobre resposta pontual.
7. VALIDACAO/DISTRIBUICAO: `validate-skills.ps1` (45/45 verdes) +
   `sincronizar-skills-ia.ps1 -Apply` (4 dists) - mesmos gates do 000118.
8. CONSUMO PELO all_IA: `/skills/sync` ja le `metadata.triggers`; a tela
   `/skills/ui` exibe registry/organograma/triggers/scripts - exibir o
   manifesto e agrupar o organograma por CAMADA e extensao natural (pedido
   ja previsto no caso 6-A do plano 000123, atividade A6 deste plano).

## Como decidir

1. Marque `[x]` na opcao escolhida de cada caso (uma por caso) - ou responda
   pela tela `/dev/ui > Incoerencias` do all_IA.
2. Se nenhuma opcao servir, descreva a sua na linha `Outra opcao`.
3. Opcionalmente preencha `Decisao do dono:` com observacoes/condicoes.

---

## Casos da rodada 1 (registro original das opcoes)

### Caso 1 - Manifesto x secoes existentes (Objetivo/Uso/Limites): onde vive o que?

- Atividades: A1, A2, A4
- Contexto: as SKILL.md ja declaram proposito (`## Objetivo`), uso
  (`## Uso`) e um escopo negativo informal (`## Limites`). Um manifesto
  completo em `metadata` duplicaria isso em duas fontes da verdade; por
  outro lado, o corpo nao e maquina-legivel para o roteador/all_IA.
- Impacto: duplicar = risco de divergencia silenciosa entre corpo e
  metadata; so corpo = continua ilegivel por maquina; so o NOVO em metadata
  = zero duplicacao e ganho maquina-legivel onde importa.

Opcoes:

- [x] A) `metadata` recebe SO o que e novo e maquina-legivel: `camada`, `escopo_negativo` (lista curta de frases), `dependencias` (nomes) e `saidas` (lista); proposito/uso continuam EXCLUSIVOS do corpo (`## Objetivo`/`## Usa`); `## Limites` permanece como texto humano e o `escopo_negativo` e o resumo maquina-legivel dele. (Recomendada - sem fonte dupla)
- [ ] B) Manifesto COMPLETO em `metadata` (proposito, escopo positivo/negativo, camada, dependencias, saidas) - corpo vira redundante e a metadata e a fonte oficial.
- [ ] C) Sem metadata: padronizar SECOES novas no corpo (`## Escopo negativo`, `## Camada`, `## Saidas`) e os consumidores parseiam o markdown.
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 2 - Camada (ferramenta/atividade/padroes) x estrutura fisica de pastas

- Atividades: A1, A4
- Contexto: as camadas propostas nao mapeiam na arvore atual
  (`core/<dominio>`, `domains/<dominio>`); ha desvios reais (ex.:
  `postgresql-support` em `tools`). Reorganizar pastas mexe nos 4 dists,
  nos registros do all_IA e nos caminhos usados por scripts.
- Impacto: declarativo = entrega imediata e o organograma agrupa por
  camada sem mover nada; fisico = arvore "fala" a hierarquia porem custo
  alto e risco de quebra de caminhos.

Opcoes:

- [x] A) Camada DECLARATIVA (`metadata.camada: ferramenta|atividade|padroes`), sem mover pastas; a estrutura fisica continua por dominio. (Recomendada - hierarquia logica sem quebrar caminhos)
- [ ] B) Declarativa AGORA + plano futuro para realocar os desvios obvios de pasta (ex.: postgresql-support -> languages).
- [ ] C) Reorganizacao fisica por camada neste plano (ferramenta/atividade/padroes como arvore).
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 3 - Dependencias: metadata x [[wikilinks]] existentes

- Atividades: A1, A4
- Contexto: o all_IA ja sincroniza `[[wikilinks]]` do corpo como
  `SkillDependency` (dependencias/dependentes na API e na tela). O manifesto
  propoe `dependencias` declaradas. Dois mecanismos para a mesma relacao
  divergem com o tempo.
- Impacto: escolher uma fonte clara evita o drift; manter os dois exige
  regra de precedencia.

Opcoes:

- [x] A) `metadata.dependencias` vira a fonte DECLARADA (nomes das skills ajudadoras); os `[[wikilinks]]` do corpo continuam validos como citacao e o consumidor (all_IA) le AMBOS (uniao, sem duplicar). (Recomendada - declarado onde e contrato, link onde e texto)
- [ ] B) Somente `[[wikilinks]]` (sem campo novo) - o manifesto referencia a convencao existente.
- [ ] C) Somente `metadata.dependencias`; wikilinks deixam de gerar relacao no all_IA.
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 4 - Enforcement do manifesto no validador

- Atividades: A2
- Contexto: o dono pediu manifesto "obrigatorio" - mas 45 skills existem e a
  populacao e gradual. O validador do sistema (quick_validate) nao pode ser
  alterado; o enforcement e no `validate-skills.ps1` local da maintain-skills.
- Impacto: bloqueante imediato quebraria 35+ skills; sem enforcement nenhum,
  o manifesto vira opcional para sempre.

Opcoes:

- [x] A) Obrigatorio para skills NOVAS (checagem no validate-skills.ps1 quando a skill nao existir no lote anterior) + AVISO (nao bloqueante) nas existentes sem manifesto; vira bloqueante geral num plano futuro apos populacao. (Recomendada - progressivo sem quebrar)
- [ ] B) Bloqueante para TODAS ja neste plano (exige popular as 45 agora).
- [ ] C) Sempre opcional (so convencao documentada).
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 5 - Protocolo de fallback: onde fica declarado?

- Atividades: A3, A4
- Contexto: hoje nenhuma skill declara o caminho de devolucao; o
  `route-skills-by-context` nao tem secao de fallback. O pedido: "fora do
  proposito -> devolve ao roteador, sem improvisar".
- Impacto: so no roteador = regra central porem skills continuam sem o
  lembrete local; em cada skill = consciencia local explicita (e o
  escopo_negativo do caso 1 da o criterio objetivo de quando devolver).

Opcoes:

- [x] A) DUPLO: secao "Roteamento e fallback" no route-skills-by-context (protocolo: skill declara fora-de-proposito -> roteador re-roteia pela camada/manifesto) + frase padrao de fallback nos `## Limites` de cada skill populada ("fora do proposito, devolver ao route-skills-by-context"). (Recomendada - regra central + consciencia local)
- [ ] B) So no roteador (protocolo central; skills nao mudam).
- [ ] C) So no padrao da maintain-skills (documentacao, sem tocar roteador nem skills).
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 6 - Lote de populacao do manifesto

- Atividades: A4
- Contexto: o plano fala "skills prioritarias". O lote do 000118 foi 10
  (core + tools de manutencao). Para a hierarquia em camadas fazer sentido
  ja na primeira rodada, as skills de FERRAMENTA (linguagens/plataformas:
  python, powershell, fastapi, alembic, redshift-sql, postgresql-support,
  databricks-notebook-pattern, excel-validation) sao as ancoras das cadeias.
- Impacto: lote pequeno entrega rapido mas a hierarquia fica incompleta;
  todas as 45 atrasa a entrega.

Opcoes:

- [x] A) Lote do 000118 (10) + skills de FERRAMENTA (~8) = ~18 skills com manifesto nesta rodada; restante em rodadas seguintes. (Recomendada - cobre as cadeias ferramenta->atividade->padroes reais)
- [ ] B) So as 10 do 000118.
- [ ] C) Todas as 45 nesta rodada.
- [ ] Outra opcao (descrever):

Decisao do dono:

### Caso 7 - Consumo pelo all_IA (atividade A6): quando?

- Atividades: A6
- Contexto: o caso 6-A do plano 000123 ja aprovou exibir o manifesto na
  tela `/skills/ui` "quando existir". O sync do all_IA ja le
  `metadata.triggers` - estender para o manifesto e pequeno; o organograma
  poderia agrupar/sinalizar por CAMADA.
- Impacto: consumir junto fecha o ciclo na mesma rodada (manifesto visivel
  e auditavel na tela); depois = duas entregas separadas.

Opcoes:

- [x] A) Na SEQUENCIA deste plano: sync do all_IA le `metadata.camada/escopo_negativo/dependencias/saidas`, a tela exibe o manifesto no detalhe da skill e o organograma ganha badge/agrupamento por camada. (Recomendada - manifesto nasce visivel)
- [ ] B) So apos a populacao completa das 45.
- [ ] C) Sem consumo por ora (apenas os arquivos das skills).
- [ ] Outra opcao (descrever):

Decisao do dono:

---

## Rodadas decididas


