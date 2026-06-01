# 000048 - Atualizar acesso das skills nas IAs Claude e Codex

- Numero: 000048
- Titulo: Atualizar acesso das skills nas IAs Claude e Codex
- Dono: skills
- Prioridade: 1
- Status: concluido
- Criado em: 2026-05-31
- Atualizado em: 2026-05-31
- Chamado: SKILLS-JZ-CH-2026-00010
- Skills relacionadas: route-skills-by-context,maintain-planner,maintain-activities,maintain-skills,register-ticket-session

## Objetivo

Validar e atualizar a distribuicao das skills oficiais para as IAs, com foco em confirmar que Claude e Codex possuem referencias acessiveis e alinhadas aos destinos gerados por `maintain-skills`.

## Escopo

- Validar estrutura das skills oficiais em `C:\codes\skills`.
- Verificar divergencias entre origem oficial e destinos `dist/claude`, `dist/codex` e ponte global do Codex.
- Aplicar sincronizacao quando houver divergencia.
- Confirmar acessibilidade basica das referencias para Claude e Codex.

## Atividades

| # | Atividade | Status | Skill executora | Saida |
|---|---|---|---|---|
| A1 | Validar roteamento, chamado e plano antes da execucao | feito | route-skills-by-context | Sessao 001 e plano 000048 criados |
| A2 | Validar estrutura das skills oficiais | feito | maintain-skills | 37 skills validas; indices validos |
| A3 | Verificar/sincronizar destinos IA Claude e Codex | feito | maintain-skills | `sincronizar-skills-ia.ps1 -Apply` executado; sem faltantes/extras |
| A4 | Confirmar referencias acessiveis para Codex e Claude | feito | maintain-skills | Codex bridge ok; Claude aponta para `C:\codes\AGENTS.md` e `dist\claude` |
| A5 | Registrar conclusao da sessao | feito | register-ticket-session | Sessao 001 movida para feitas |

## Criterios de aceite

1. Validacao de skills executada sem falha bloqueante ou com falhas registradas.
2. Destinos `dist/claude` e `dist/codex` conferidos e atualizados quando necessario.
3. Ponte global do Codex validada como acessivel.
4. Evidencia registrada na sessao do chamado.

## Skills recomendadas atuais

- maintain-skills
- route-skills-by-context
- maintain-planner
- maintain-activities
- register-ticket-session

## Riscos

- O sincronizador pode alterar muitos arquivos em `dist/`; validar antes de finalizar.
- A ponte Claude pode depender de convencao local diferente da ponte global do Codex; registrar evidencia em vez de presumir.