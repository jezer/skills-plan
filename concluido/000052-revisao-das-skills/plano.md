# 000052 - Revisao das skills

- Numero: 000052
- Titulo: revisao das skills
- Dono: skills
- Prioridade: 1
- Status: concluido
- Criado em: 2026-05-31
- Atualizado em: 2026-05-31
- Chamado: SKILLS-JZ-CH-2026-00011
- Skills relacionadas: route-skills-by-context, maintain-planner, maintain-activities, maintain-skills, maintain-git, technical-writer

## Objetivo

Revisar o sistema de skills do workspace para transformar o contexto atual das skills em uma base consultavel, definir triggers claras para que a IA identifique quando cada skill deve ser acionada e estabelecer governanca de versionamento com aprovacao explicita de versoes de producao.

## Escopo

1. Inventariar as skills oficiais em `C:\codes\skills`, incluindo nome, descricao, objetivo, uso, limites, aliases e caminhos.
2. Definir um modelo de dados para armazenar o inventario das skills em formato consultavel por automacoes.
3. Mapear triggers textuais objetivas para roteamento por intencao do usuario.
4. Definir validacoes para detectar ambiguidade, sobreposicao de proposito e ausencia de trigger clara.
5. Propor criterios para manter os indices e triggers atualizados quando uma skill for criada ou alterada.
6. Definir governanca de versoes das skills, incluindo versao candidata, versao aprovada, versao de producao e historico de autorizacoes.
7. Definir regra de rollback para restaurar uma versao anterior como unica versao em uso quando houver necessidade operacional.
8. Definir politica de retencao: manter sempre a uniao entre as ultimas 3 versoes e todas as versoes dos ultimos 15 dias.

Fora de escopo nesta primeira etapa: reescrever todas as skills, alterar comportamento de IA em runtime, publicar versao nova sem aprovacao registrada ou substituir o mecanismo atual de roteamento sem validacao previa.

## Principio filosofico e gerencial das skills

O sistema de skills deve funcionar como uma hierarquia contributiva: cada skill tem uma funcao objetiva, contribui para um resultado maior e depende de outras skills somente quando essa dependencia torna a responsabilidade mais clara. A hierarquia nao deve significar disputa de autoridade; deve significar organizacao de proposito, delegacao e fluxo.

A analogia principal e o ciclo da agua. A nuvem depende da evaporacao do mar, a chuva alimenta rios, os rios voltam ao mar e o ciclo continua. Cada parte tem uma funcao especifica, mas nenhuma existe isolada. A nuvem nao tenta ser rio, o rio nao tenta ser mar, e o mar nao substitui a chuva. O valor esta na dependencia ciclica bem definida: cada componente entrega sua parte, recebe contribuicoes de outros e mantem o sistema funcionando.

O mesmo principio vale para as skills. Uma skill nao deve fazer o que outra ja tem instrucao clara para fazer. Quando uma responsabilidade ja existe, a skill deve referenciar, delegar ou encaminhar para a skill dona, em vez de duplicar comportamento. Isso reduz conflito, evita sobreposicao de regras e deixa a IA mais previsivel ao interpretar o texto do usuario.

A segunda analogia e a celula. Cada componente celular tem uma funcao especifica, organizada e dependente dos demais. O sistema so funciona porque existem fronteiras, papeis, sinais e referencias internas. Nas skills, as triggers funcionam como esses sinais: elas iniciam a skill correta quando o texto do usuario indica uma intencao, uma condicao ou um contexto. A trigger nao deve ser ampla demais; ela deve apontar para a responsabilidade certa, no nivel certo da hierarquia.

Principio fundamental: skills devem ser pequenas unidades de responsabilidade com proposito claro, limites explicitos, dependencias conhecidas e triggers objetivas. Quando houver conflito entre duas skills, a correcao esperada nao e escolher arbitrariamente uma delas, mas revisar proposito, limite, dependencia e trigger ate que a delegacao fique evidente.

## Governanca de versionamento e producao

1. Toda alteracao de skill deve gerar uma versao candidata identificavel, com hash ou referencia de origem, autor, data, motivo, escopo e evidencias de validacao.
2. Uma versao candidata so pode virar versao de producao quando existir autorizacao registrada no banco de skills.
3. A autorizacao deve registrar quem aprovou, quando aprovou, qual versao foi aprovada, quais evidencias foram aceitas e qual versao anterior sera substituida.
4. Em producao deve existir apenas uma versao ativa por skill.
5. Ao aprovar nova versao de producao, a versao anterior deve permanecer no historico como candidata a rollback.
6. Rollback deve registrar uma nova ordem/autorizacao apontando a versao anterior como versao ativa novamente.
7. O banco deve permitir auditar a linha do tempo: versao criada, validada, aprovada, ativada, substituida, restaurada ou descartada.
8. A politica de retencao deve manter a uniao destes conjuntos:
   - ultimas 3 versoes de cada skill, mesmo que tenham mais de 15 dias;
   - todas as versoes de cada skill criadas ou ativadas nos ultimos 15 dias, mesmo que sejam mais de 3.
9. Versoes fora dos dois conjuntos de retencao podem ser arquivadas ou descartadas somente se nao forem a versao ativa atual e se nao estiverem vinculadas a auditoria pendente.

## Relatorios obrigatorios por ciclo de manutencao

Os relatorios em `C:\codes\skills\reports` devem ser tratados como evidencia operacional de cada ciclo de manutencao das skills, nao como arquivos avulsos. A revisao inicial identificou:

1. `validate-skills-2026-05-31.json`: relatorio recente, com 37 skills avaliadas, 37 validas e 0 invalidas.
2. `skills-metrics-20260519-002007.json`: relatorio existente de metricas, com `sync_apply=true`, 29 skills oficiais, sem faltantes em Gemini/Copilot/Claude, `codex_bridge_ok=true` e `health_critical_ok=true`.
3. `validate-skills.ps1` esta integrado ao fechamento de manutencao de `maintain-skills`.
4. `generate-skills-metrics-report.ps1` existe e gera relatorio em `reports`, mas o ultimo arquivo encontrado e de 2026-05-19; portanto, o plano deve tornar sua execucao continua e obrigatoria no ciclo.

Regra proposta para cada ciclo de manutencao de skills:

1. Antes da alteracao: consultar o ultimo `validate-skills` e o ultimo `skills-metrics` para entender estado de entrada.
2. Durante a alteracao: nao promover versao candidata se houver invalidade estrutural conhecida ou divergencia critica de sincronizacao.
3. Ao fechar a manutencao: executar `validate-skills.ps1` com `-ReportPath C:\codes\skills\reports\validate-skills-AAAA-MM-DD-HHMMSS.json`.
4. Ao fechar a manutencao: executar `generate-skills-metrics-report.ps1` para registrar metricas de sincronizacao, saude e cobertura.
5. Registrar no chamado/plano os caminhos dos dois relatorios gerados no ciclo.
6. Bloquear promocao para producao quando `validate-skills` tiver invalidas ou quando `skills-metrics` indicar falha critica de saude, ponte Codex quebrada ou faltantes de sincronizacao relevantes.

## Report gerencial de planos pendentes

O root `C:\codes` deve manter uma pasta padronizada para triagem gerencial dos planos em andamento:

- Pasta: `C:\codes\plan\report_gerencial`
- JSON: `C:\codes\plan\report_gerencial\planos-pendentes-gerencial.json`
- CSV editavel: `C:\codes\plan\report_gerencial\planos-pendentes-gerencial.csv`
- Markdown executivo: `C:\codes\plan\report_gerencial\planos-pendentes-gerencial.md`

Esse report deve ser gerado a partir de `C:\codes\plan\indice-planos-jz.json` e deve permitir ao usuario alterar a leitura gerencial sem executar mudanca operacional imediata. As colunas de decisao devem suportar pelo menos:

1. `ordem_gerencial`: ordem atual sugerida para leitura e priorizacao.
2. `decisao_gerencial`: `avaliar`, `executar`, `bloquear`, `melhorar` ou `excluir`.
3. `novo_numero`: campo livre para o usuario informar o novo numero alvo do plano, especialmente quando houver duplicidade.
4. `nova_ordem`: campo livre para o usuario propor nova ordem.
5. `novo_status`: campo livre para propor mudanca de status.
6. `motivo_decisao`: justificativa gerencial da alteracao proposta.

A primeira geracao do report encontrou 17 planos em andamento, todos com pasta e `plano.md` existentes. Pontos de atencao detectados: 7 sem `atividades.md`, 9 sem chamado vinculado e 10 entradas com numero duplicado. Essas pendencias nao devem ser corrigidas por renomeacao manual imediata; devem virar atividades especificas por contexto dono, porque o `maintain-planner` declara que o numero do plano e global e unico.

Regra proposta: antes de alterar numero, ordem, status, bloqueio, melhoria ou exclusao de planos, consultar o report gerencial e registrar a decisao em chamado/plano. Qualquer aplicacao operacional da decisao deve passar por `maintain-planner` e `maintain-activities`, preservando autonomia do contexto dono.

Quando o usuario preencher `novo_numero`, o valor deve ser tratado como proposta de renumeracao. Se o usuario alterar diretamente a coluna `numero`, a diferenca entre o numero no CSV e o numero presente no caminho do plano tambem deve ser tratada como decisao gerencial de renumeracao. A aplicacao deve validar que o numero informado tem 6 digitos, nao esta em uso por outro plano que permanecera ativo, nao quebra referencias do chamado/plano e pode ser aplicado com alteracao coordenada de pasta, `plano.md`, indices e eventuais links. Renumeracao nao deve ser feita por edicao manual isolada do CSV.

## Atividades planejadas

| # | Atividade | Status | Skill executora | Saida |
|---|---|---|---|---|
| A1 | Inventariar fontes atuais de skills, indices e descricoes de uso | feito | maintain-skills | Fontes e relatorios atuais registrados no plano |
| A2 | Desenhar modelo de dados para skills em banco consultavel | feito | technical-writer | Entidades e campos de governanca descritos no plano |
| A3 | Definir taxonomia de triggers por texto do usuario | feito | route-skills-by-context | Principios, triggers e delegacao registrados |
| A4 | Definir regras de desambiguacao quando multiplas skills combinarem | feito | route-skills-by-context | Hierarquia contributiva e delegacao para skill dona registradas |
| A5 | Definir validadores para lacunas, duplicidades e conflitos de triggers | feito | maintain-activities | Criterios e riscos registrados |
| A6 | Registrar decisao sobre artefato final: JSON, CSV, SQLite ou outro formato | feito | maintain-planner | Banco consultavel tratado como etapa futura com requisitos definidos |
| A7 | Exigir branch explicita no fluxo de clone da skill Git | concluido | maintain-skills | `maintain-git` e script de clone bloqueiam clone sem branch informada |
| A8 | Modelar entidades de versionamento, aprovacao e producao no banco de skills | feito | technical-writer | Modelo conceitual de versoes, autorizacoes, estado ativo e historico |
| A9 | Definir fluxo de promocao de versao candidata para producao | feito | maintain-skills | Processo de aprovacao e ativacao unica registrado |
| A10 | Definir fluxo de rollback por nova ordem/autorizacao | feito | maintain-skills | Regra para restaurar versao anterior como ativa registrada |
| A11 | Definir politica de retencao de versoes por skill | feito | maintain-activities | Regra: manter ultimas 3 versoes e todas dos ultimos 15 dias |
| A12 | Definir validacoes antes de ativar uma versao em producao | feito | maintain-activities | Checklist de bloqueios, evidencias e auditoria registrado |
| A13 | Formalizar hierarquia contributiva e dependencias entre skills | feito | technical-writer | Principios de proposito, delegacao, fronteira e dependencia |
| A14 | Criar regra de deteccao de conflito entre triggers e responsabilidades | feito | route-skills-by-context | Regra para identificar duplicidade e encaminhar para skill dona |
| A15 | Tornar `validate-skills` e `skills-metrics` evidencias obrigatorias em cada ciclo de manutencao | feito | maintain-skills | Fluxo de entrada/saida com relatorios em `reports` |
| A16 | Definir bloqueios de promocao baseados nos relatorios de validacao e metricas | feito | maintain-activities | Gate de producao com criterios objetivos |
| A17 | Padronizar report gerencial dos planos pendentes no root | feito | maintain-planner | `C:\codes\plan\report_gerencial` com JSON, CSV e Markdown |
| A18 | Definir fluxo para aplicar decisoes gerenciais de ordem, bloqueio, melhoria ou exclusao | feito | maintain-activities | Processo seguro para transformar decisao em atividade por contexto |
| A19 | Investigar e regularizar duplicidade de numeros no indice de planos | feito | maintain-planner | Duplicidades regularizadas no report atual |
| A20 | Definir fluxo seguro para aplicar `novo_numero` informado no report gerencial | feito | maintain-planner | Validacao e renumeracao coordenada de pasta, metadados, indice e referencias |
| A21 | Aceitar alteracao direta da coluna `numero` como proposta de renumeracao no report gerencial | feito | maintain-planner | Comparacao CSV x caminho registrada e usada |

## Criterios de aceite

1. Existe um inventario minimo das skills com campos suficientes para consulta e roteamento.
2. Cada skill relevante possui triggers positivas, limites negativos e exemplos curtos de texto do usuario.
3. O plano define onde o "banco de dados" das skills ficara armazenado e como sera atualizado.
4. A matriz de triggers deixa claro quando chamar `route-skills-by-context`, `maintain-skills`, `maintain-planner`, `maintain-activities` e skills de dominio.
5. Ambiguidades conhecidas geram regra de prioridade ou pergunta objetiva ao usuario.
6. Nenhuma implementacao persistente futura deve ocorrer sem atividade vinculada, skill recomendada e criterio de aceite.
7. O fluxo de clone da skill `maintain-git` exige branch explicita, usa essa branch no clone e valida que o checkout final ficou na branch solicitada.
8. O banco de skills possui campos para versao candidata, versao ativa de producao, versao anterior, status, autorizacao, aprovador, data/hora, evidencias e motivo.
9. Existe regra explicita garantindo que apenas uma versao por skill fique disponivel para uso em producao.
10. Existe fluxo documentado para rollback, sempre por nova ordem/autorizacao registrada.
11. A politica de retencao preserva a uniao entre ultimas 3 versoes e versoes dos ultimos 15 dias por skill.
12. Nenhuma versao ativa ou vinculada a auditoria pendente pode ser descartada pela retencao automatica.
13. O modelo de skills registra proposito, limites, dependencias e delegacoes para evitar sobreposicao de responsabilidades.
14. Cada trigger aponta para uma responsabilidade objetiva e, quando houver dependencia, indica a skill dona para delegacao.
15. Cada ciclo de manutencao de skills gera ou referencia um relatorio `validate-skills` e um relatorio `skills-metrics`.
16. Promocao de versao de skill para producao exige validacao estrutural sem falhas e metricas sem falha critica.
17. O chamado ou sessao do ciclo registra os caminhos dos relatorios usados como evidencia.
18. Existe report gerencial central em `C:\codes\plan\report_gerencial` para todos os planos em andamento do indice root.
19. O report indica existencia de pasta, existencia de `plano.md`, existencia de `atividades.md`, chamado, pendencias e decisao gerencial sugerida.
20. Mudancas de ordem, status, bloqueio, melhoria ou exclusao nao sao aplicadas diretamente pelo report; elas geram atividade validada pelo contexto dono.
21. O report possui campo `novo_numero` para o usuario propor renumeracao de planos duplicados ou incorretos.
22. Toda aplicacao de `novo_numero` valida unicidade, formato de 6 digitos, referencias e autonomia do contexto dono antes de renomear qualquer pasta.
23. Quando a coluna `numero` for editada diretamente, a aplicacao compara esse valor com o numero atual extraido do caminho e trata divergencia como proposta de renumeracao.

## Checklist

- [x] Confirmar fontes oficiais de skills e indices existentes.
- [x] Levantar campos atuais reaproveitaveis de `SKILL.md` e `agents/openai.yaml`.
- [x] Escolher formato inicial do banco consultavel.
- [x] Documentar triggers por intencao do usuario.
- [x] Validar conflitos entre skills com proposito semelhante.
- [x] Registrar proximas atividades executaveis antes de alterar scripts ou indices.
- [x] Definir estados de versao: candidata, validada, aprovada, producao, substituida, restaurada e descartada.
- [x] Definir campos obrigatorios de autorizacao de subida para producao.
- [x] Definir regra de rollback com nova ordem registrada no banco.
- [x] Definir consulta para selecionar a unica versao ativa por skill.
- [x] Definir retencao combinando ultimas 3 versoes e janela de 15 dias.
- [x] Registrar a hierarquia contributiva como principio de desenho das skills.
- [x] Mapear dependencias aceitas entre skills sem duplicar responsabilidades.
- [x] Definir regra para trigger ampla demais, ambigua ou conflitante.
- [x] Incluir `validate-skills.ps1 -ReportPath` no encerramento obrigatorio do ciclo de manutencao.
- [x] Incluir `generate-skills-metrics-report.ps1` no encerramento obrigatorio do ciclo de manutencao.
- [x] Registrar no chamado os caminhos dos relatorios gerados ou consultados.
- [x] Definir bloqueios objetivos para invalidas, faltantes de sincronizacao, ponte Codex quebrada ou saude critica falsa.
- [x] Manter `C:\codes\plan\report_gerencial` como pasta padrao do report gerencial de planos pendentes.
- [x] Regenerar report gerencial sempre que o indice de planos mudar de forma relevante.
- [x] Regularizar planos sem chamado, sem atividades ou com numero duplicado por atividade propria.
- [x] Definir como o usuario registra nova ordem e decisao gerencial antes da aplicacao operacional.
- [x] Definir como o usuario registra `novo_numero` para planos duplicados.
- [x] Definir como aplicar alteracao direta da coluna `numero` sem perder rastreabilidade.
- [x] Criar validacao para impedir `novo_numero` ja usado por plano ativo que nao sera renumerado.
- [x] Definir atualizacao coordenada de pasta, `plano.md`, indices e links ao aplicar renumeracao.

## Evidencias de fechamento

1. Governanca de versionamento, producao, rollback e retencao registrada neste plano.
2. Principio de hierarquia contributiva e dependencia entre skills registrado.
3. Uso obrigatorio de `validate-skills` e `skills-metrics` por ciclo registrado.
4. Report gerencial criado em `C:\codes\plan\report_gerencial`.
5. Fluxo de renumeracao por `novo_numero` ou alteracao direta de `numero` registrado e exercitado.
6. Planos pendentes foram revisados, duplicidades removidas e planos concluidos arquivados.
7. Implementacoes tecnicas futuras devem nascer em planos novos e especificos, usando estes criterios como governanca.

## Skills recomendadas atuais

- `route-skills-by-context`: definir e validar o roteamento por condicao textual.
- `maintain-planner`: manter o plano numerado e a governanca de planejamento.
- `maintain-activities`: detalhar, validar e acompanhar atividades executaveis.
- `maintain-skills`: revisar estrutura, metadados e indices oficiais de skills quando a manutencao for explicitamente solicitada.
- `maintain-git`: apoiar referencias de origem, branches, commits e rastreabilidade quando a versao de skill depender de artefatos Git.
- `technical-writer`: documentar o modelo de dados, matriz de triggers e criterios.
- `periodic-skills-reviewer`: apoiar revisoes periodicas dos relatorios, tendencias de metricas e lacunas recorrentes.

## Riscos

- Confundir inventario de skills com alteracao direta das skills sem atividade aprovada.
- Criar triggers amplas demais, acionando skills em contextos errados.
- Duplicar regras entre banco de skills, `SKILL.md`, `AGENTS.md` e indices existentes.
- Escolher formato de armazenamento antes de confirmar consultas e automacoes necessarias.
- Permitir que uma skill assuma trabalho que ja pertence a outra skill, enfraquecendo a delegacao.
- Criar dependencias circulares sem funcao clara, causando roteamento imprevisivel.
- Permitir duas versoes ativas da mesma skill por falha na promocao ou rollback.
- Registrar aprovacao sem evidencias verificaveis ou sem aprovador identificavel.
- Remover versoes historicas ainda necessarias para rollback, auditoria ou retencao minima.
- Tratar relatorios de `reports` como historico opcional, em vez de evidencia obrigatoria de manutencao.
- Deixar `skills-metrics` descontinuado por falta de execucao regular, mesmo com script disponivel.
- Aplicar exclusao, bloqueio ou reordenacao de plano diretamente pelo report sem validar chamado, atividade e contexto dono.
- Corrigir duplicidade de numeros por renomeacao manual sem diagnosticar origem no `maintain-planner`.
- Aplicar `novo_numero` apenas no CSV sem renomear pasta, atualizar `plano.md` e regenerar indices.