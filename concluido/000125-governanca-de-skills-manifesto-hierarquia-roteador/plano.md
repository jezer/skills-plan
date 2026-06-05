# 000125 - governanca de skills manifesto hierarquia roteador

- Numero: 000125
- Titulo: governanca de skills manifesto hierarquia roteador
- Dono: skills
- Usuario atual: jz
- Prioridade: 2
- Status: concluido
- Criado em: 2026-06-04
- Atualizado em: 2026-06-04 (concluido)
- Chamado: TOOLS-JZ-CH-2026-00123
- Skills relacionadas: maintain-skills, route-skills-by-context, periodic-skills-reviewer
- Origem: PEDIDO cross-contexto do Ajuste 7 do plano `tools/all_IA/plan/000123-melhorar-menu` (decisao caso 6-A; precedente: plano 000118)

## Objetivo

Governanca da biblioteca de skills: dar as skills consciencia de escopo via
CONTRATO/MANIFESTO, hierarquia em camadas e roteamento/fallback disciplinado.

## Fundamento (conteudo integral do pedido do dono)

O que incomoda: as skills nao tem consciencia de escopo - nao distinguem o
que e certo/errado para o contexto. Faltam: (1) escopo NEGATIVO explicito;
(2) hierarquia e delegacao claras (quando consultar outra skill ou devolver
ao roteador); (3) padronizacao de saida (sem reuso). Resultado: baixa
coesao, acoplamento implicito, respostas fora de proposito.

Como deve ser:
1. Responsabilidade unica e contexto delimitado (SRP + Bounded Context).
2. CONTRATO/MANIFESTO obrigatorio por skill declarando: proposito, escopo
   positivo, escopo NEGATIVO (o que NAO pode fazer), dependencias (skills
   ajudadoras) e saidas esperadas.
3. Hierarquia em camadas (composicao, nao duplicacao), dependencia de cima
   para baixo: Skill de FERRAMENTA (ex.: Redshift - conhecimento amplo, sem
   especializacao; ao receber algo especifico orienta criar skill focada) ->
   Skill de ATIVIDADE (resolve atividade concreta consultando a de
   Ferramenta) -> Skill de PADROES (aplica convencoes consultando Atividade
   e Ferramenta).
4. Roteamento e fallback (router/dispatcher): demanda fora do proposito NAO
   se improvisa - devolve ao `route-skills-by-context`, unico orquestrador;
   as skills apenas declaram "isto nao e meu proposito".
5. Saidas parametrizadas e reutilizaveis (DRY): priorizar scripts
   parametrizados/idempotentes em vez de respostas pontuais.
6. Coesao alta, acoplamento baixo: nenhuma skill fura camadas; quem
   desconhece o destino encaminha ao roteador.

Referencias: SOLID/SRP, Separation of Concerns, Bounded Context (DDD),
padroes Router/Dispatcher, Agent Skills com composicao e delegacao.

## Escopo

1. Definir o formato do MANIFESTO no padrao de SKILL.md - campos dentro de
   `metadata` (mesmo caminho aprovado no 000118 para triggers, que o
   validador padrao aceita): proposito, escopo_positivo, escopo_negativo,
   camada (ferramenta|atividade|padroes), dependencias, saidas.
2. Atualizar `maintain-skills` (padrao + validadores) para o manifesto
   opcional-progressivo (obrigatorio em skills novas; populacao gradual nas
   existentes).
3. Atualizar `route-skills-by-context` com a regra de fallback formal
   ("fora do proposito -> devolve ao roteador").
4. Popular o manifesto nas skills prioritarias (mesmo lote do 000118).
5. Redistribuir dist/ e validar.
6. Pedido de volta ao contexto tools/all_IA: exibir o manifesto na tela
   `/skills/ui` quando existir (caso 6-A do 000123).

## Avaliacao de conflitos

Rodada 1 DECIDIDA (7 casos, todos opcao A) e executada. Incoerencia extra
corrigida: Fluxo da maintain-skills contradizia o frontmatter oficial.

## Atividades planejadas

| # | Atividade | Status | Skill executora | Saida |
|---|---|---|---|---|
| A1 | Definir formato do manifesto (metadata.*) no padrao de SKILL.md | concluido | maintain-skills | secao no padrao + exemplo |
| A2 | Validadores aceitam/validam o manifesto | concluido | maintain-skills | validate-skills.ps1 |
| A3 | Regra de fallback formal no route-skills-by-context | concluido | route-skills-by-context | secao de roteamento/fallback |
| A4 | Popular manifesto nas skills prioritarias | concluido | maintain-skills | lote com manifesto |
| A5 | Redistribuir dist/ e validar consumo | concluido | maintain-skills | dists coerentes |
| A6 | Consumo pelo all_IA: exibir manifesto em /skills/ui | concluido | maintain-planner | atividade no contexto tools/all_IA |

## Criterio de aceite

1. Manifesto documentado no padrao e aceito pelos validadores (45/45 verdes).
2. Skills prioritarias com escopo negativo e camada declarados.
3. `route-skills-by-context` com fallback explicito.
4. Dists redistribuidos sem faltas/extras.

## Checklist

- [x] Formato do manifesto definido (A1).
- [x] Validadores atualizados (A2).
- [x] Fallback no roteador (A3).
- [x] Skills prioritarias com manifesto (A4).
- [x] Redistribuicao validada (A5).
- [x] Pedido de exibicao no all_IA (A6).

## Skills recomendadas atuais

- maintain-skills (dona do padrao e validadores)
- route-skills-by-context (roteador)
- periodic-skills-reviewer (revisao de aderencia)

## Riscos

1. Manifesto extenso demais virar burocracia: campos curtos e objetivos.
2. Divergencia fontes x dist sem redistribuicao: A5 obrigatoria.

## Validacao planejada

1. `validate-skills.ps1` verde apos cada lote.
2. Redistribuicao via `sincronizar-skills-ia.ps1 -Apply`.