Plano: Controle de Índices por Usuário

Objetivo
- Manter índices por máquina/usuário (index-<user>.json) e permitir sincronização via Git entre máquinas.
- Garantir que o global do Copilot sempre carregue as skills atualizadas de C:\\codes\\skills\\dist\\copilot.

Visão geral
- Cada máquina tem C:\\codes\\skills\\indices\\index-<user>.json (ex: index-jz.json).
- Um script de mesclagem (merge_indices.ps1) combina todos os index-*.json em C:\\codes\\skills\\skills.json (canônico) e publica em dist\\copilot.
- Nome do índice local usa usuario atual (padrao "jz").

Padrões e convenções
- Diretório de índices: C:\\codes\\skills\\indices\\
- Nome de arquivo: index-<usuario>.json (ex: index-jz.json)
- Formato: JSON array de objetos skill com campo "id" (string), "name", "version", "maturity", "owner", "last_reviewed" (ISO8601 opcional).

Fluxo operacional
1) Na sessão: executar session-bootstrap.ps1 que valida chamado_id e garante leitura de C:\\codes\\skills\\dist\\copilot antes de qualquer ação.
2) Produzir/atualizar index-<user>.json localmente e commitar em repo (pull/push para sincronizar).
3) Executar merge_indices.ps1 localmente (automação CI também pode executar em push) para gerar skills.json canônico e copiar para dist\\copilot.
4) Validar com validate-skills.ps1 (--check) e abrir PR para mudanças de larga escala.

Segurança e segurança de dados
- Scripts criam backups: .from-merge-<timestamp>.json antes de sobrescrever.
- Tokens e credenciais nunca escritos em índices.

Critérios de aceite
- Após execução, C:\\codes\\skills\\skills.json existe e contém a união deduplicada de todos os index-*.json.
- C:\\codes\\skills\\dist\\copilot\\skills.json atualizado e backup criado.
- session-bootstrap impede ações se dist\\copilot não for legível.

Próximos passos imediatos
- Criar pasta indices e um index-jz.json inicial (vazio [])
- Rodar merge_indices.ps1 (verificar e commitar)
- Adicionar pre-session bootstrap ao plano e ao chamado

Arquivo criado para revisão: C:\\codes\\skills\\plan\\plan_index_control.md
