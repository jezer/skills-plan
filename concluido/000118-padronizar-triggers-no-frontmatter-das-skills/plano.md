# 000118 - padronizar triggers no frontmatter das skills

- Numero: 000118
- Titulo: padronizar triggers no frontmatter das skills
- Dono: skills
- Usuario atual: jz
- Prioridade: 3
- Status: concluido
- Criado em: 2026-06-03
- Atualizado em: 2026-06-04
- Chamado: TOOLS-JZ-CH-2026-00009
- Skills relacionadas: maintain-skills, route-skills-by-context
- Origem: PEDIDO cross-contexto do plano `tools/all_IA/plan/000113-design-melhor` (DM-21, decisao rodada 2 caso 5-B)

## Objetivo

Padronizar a declaracao de gatilhos (triggers) nas SKILL.md do workspace via
campo `triggers:` no frontmatter, para que o sync do `all_IA` (e qualquer outro
consumidor) leia os gatilhos de forma DECLARADA, sem heuristica sobre a
`description`.

## Escopo

1. Definir o formato oficial no padrao de SKILL.md (lista YAML):
   `triggers:` seguido de itens `- <frase gatilho>`.
2. Atualizar a skill dona do padrao (`maintain-skills`) e seus validadores para
   aceitar/validar o campo opcional `triggers:`.
3. Popular gradualmente o campo nas SKILL.md existentes (45 fontes em
   core/domains), comecando pelas skills mais roteadas.
4. Redistribuir as copias `dist/` apos a mudanca (sincronizar-skills-ia.ps1).

## Arquivos/pastas afetados

- `C:\codes\skills\core\**\SKILL.md` e `C:\codes\skills\domains\**\SKILL.md`
- `C:\codes\skills\core\skill_registry\maintain-skills\scripts\validate-skills.ps1`
- `C:\codes\skills\dist\*` (via redistribuicao)

## Dependencias

- Consumidor ja pronto: `tools/all_IA` le `triggers:` do frontmatter no
  `POST /skills/sync` (plano 000113, DM-21). Sem o campo, zero triggers - sem erro.

## Atividades

| # | Atividade | Status | Skill executora | Saida |
|---|---|---|---|---|
| A1 | Definir formato oficial do campo `triggers:` no padrao de SKILL.md | concluido | maintain-skills | secao no padrao + exemplo |
| A2 | Atualizar validadores do maintain-skills para o campo opcional | concluido | maintain-skills | validate-skills.ps1 aceita/valida triggers |
| A3 | Popular `triggers:` nas SKILL.md prioritarias | concluido | maintain-skills | skills com gatilhos declarados |
| A4 | Redistribuir dist/ e validar leitura pelo all_IA (`/skills/sync` + `/skills/triggers`) | concluido | maintain-skills | triggers visiveis na API do all_IA |

## Criterios de aceite

1. Padrao de SKILL.md documenta o campo `triggers:` (opcional, lista YAML).
2. Validador aceita skills com e sem o campo.
3. `POST /skills/sync` no all_IA popula `SkillTrigger`/`SkillTriggerLink` a partir das SKILL.md atualizadas.
4. Nenhuma skill quebrada pela mudanca (validate-skills.ps1 verde).

## Skills recomendadas atuais

- maintain-skills (executora do padrao e validadores)
- route-skills-by-context (roteamento obrigatorio)

## Riscos

- Divergencia entre fontes e dist/ se a redistribuicao nao rodar apos popular o campo.
- Triggers redundantes com a description; manter frases curtas e acionaveis.

## Validacao planejada

1. `validate-skills.ps1` verde apos cada lote.
2. `POST /skills/sync` no all_IA e conferencia em `GET /skills/triggers`.


## Registro de execucao (2026-06-04)

1. INCOERENCIA RESOLVIDA no A1: o validador padrao de skills
   (`quick_validate.py` do skill-creator) so permite `name/description/
   license/allowed-tools/metadata` no frontmatter - `triggers:` no topo seria
   INVALIDO. Formato oficial adotado: `metadata.triggers` (lista YAML),
   documentado na secao "Triggers (gatilhos)" da `maintain-skills`.
2. A2: nenhum ajuste necessario no validate-skills.ps1 (metadata e permitido);
   validacao completa: 45/45 skills validas.
3. A3: `metadata.triggers` populado em 10 skills prioritarias
   (maintain-planner, maintain-activities, route-skills-by-context,
   maintain-skills, periodic-skills-reviewer, maintain-git,
   maintain-filesystem, maintain-tickets, register-ticket-session,
   maintain-agents) - 36 gatilhos.
4. A4: redistribuicao via `sincronizar-skills-ia.ps1 -Apply` (45 fontes ->
   4 dists sem faltas/extras); consumidor all_IA atualizado para ler
   `metadata.triggers` (alem do topo) com teste proprio; sync fim-a-fim
   leu 36 triggers/36 vinculos.