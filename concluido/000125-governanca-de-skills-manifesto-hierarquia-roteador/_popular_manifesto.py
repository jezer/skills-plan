"""Plano 000125 A4: popula metadata.camada/escopo_negativo/dependencias/saidas
no lote de 18 skills (decisoes 1-A/2-A/3-A/5-A/6-A) + frase de fallback nos Limites."""
import io
import re
from pathlib import Path

ROOT = Path(r"C:\codes\skills")
FALLBACK = "Fora do proposito desta skill, devolver ao `route-skills-by-context` (nao improvisar)."

LOTE = {
    # ── 10 do 000118 ──
    "core/skill_registry/maintain-skills": {
        "camada": "padroes",
        "escopo_negativo": [
            "nao cria nem conclui planos (maintain-planner)",
            "nao executa operacoes git (maintain-git)",
            "nao roteia demandas (route-skills-by-context)",
        ],
        "dependencias": ["powershell-specialist"],
        "saidas": ["validate-skills.ps1", "sincronizar-skills-ia.ps1", "SKILL.md normalizado no padrao"],
    },
    "core/planner/maintain-planner": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao implementa o codigo das atividades planejadas",
            "nao cria chamados (maintain-tickets)",
            "nao conclui plano sem criterios de aceite verificados",
        ],
        "dependencias": ["maintain-activities", "maintain-tickets"],
        "saidas": ["criar-plano.ps1", "validar-plano.ps1", "concluir-plano.ps1", "indice de planos regenerado"],
    },
    "core/planner/maintain-activities": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao cria planos (maintain-planner)",
            "nao executa mudancas tecnicas persistentes",
        ],
        "dependencias": ["maintain-planner"],
        "saidas": ["atividades detalhadas com skill executora", "validar-roteamento-obrigatorio.ps1"],
    },
    "core/router/route-skills-by-context": {
        "camada": "padroes",
        "escopo_negativo": [
            "nao implementa mudancas persistentes por conta propria",
            "nao substitui as skills donas da execucao",
        ],
        "dependencias": [],
        "saidas": ["selecionar-skills.ps1", "registro de roteamento na sessao"],
    },
    "core/validator/periodic-skills-reviewer": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao altera skills diretamente (propoe via maintain-skills)",
            "nao valida planos (maintain-planner)",
        ],
        "dependencias": ["maintain-skills"],
        "saidas": ["relatorio periodico de aderencia das skills"],
    },
    "domains/tools/maintain-agents": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao edita SKILL.md (maintain-skills)",
            "nao executa operacoes git (maintain-git)",
        ],
        "dependencias": ["maintain-skills"],
        "saidas": ["AGENTS.md normalizados por contexto"],
    },
    "domains/tools/maintain-filesystem": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao decide estrutura de planos/skills (skills donas)",
            "nao remove arquivos sem rastreabilidade",
        ],
        "dependencias": ["powershell-specialist"],
        "saidas": ["estrutura de pastas padronizada do workspace"],
    },
    "domains/tools/maintain-git": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao commita em branch protegida sem branch de trabalho",
            "nao gerencia chamados (maintain-tickets)",
            "nao decide conteudo funcional das mudancas",
        ],
        "dependencias": ["powershell-specialist", "connect-github-gitlab"],
        "saidas": ["commit-push.ps1", "commitar-todos-repos.ps1", "indice de repositorios"],
    },
    "domains/tools/maintain-tickets": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao cria planos (maintain-planner)",
            "nao implementa a solucao do chamado",
        ],
        "dependencias": ["maintain-filesystem"],
        "saidas": ["estrutura de chamado com sessoes", "indices de chamados"],
    },
    "domains/tools/register-ticket-session": {
        "camada": "atividade",
        "escopo_negativo": [
            "nao cria chamados (maintain-tickets)",
            "nao decide o roteamento (registra o que route-skills-by-context decidiu)",
        ],
        "dependencias": ["maintain-tickets", "route-skills-by-context"],
        "saidas": ["sessoes registradas em sessoes/feitas e pendentes"],
    },
    # ── 8 skills de FERRAMENTA (ancoras das cadeias) ──
    "domains/languages/python-specialist": {
        "camada": "ferramenta",
        "escopo_negativo": [
            "nao resolve atividade especifica de empresa (orientar criacao de skill de atividade)",
            "nao decide arquitetura de projeto",
            "nao executa operacoes git (maintain-git)",
        ],
        "dependencias": [],
        "saidas": ["codigo python idiomatico", "scripts argparse parametrizados e idempotentes"],
    },
    "domains/languages/powershell-specialist": {
        "camada": "ferramenta",
        "escopo_negativo": [
            "nao resolve atividade especifica de empresa (orientar criacao de skill de atividade)",
            "nao decide fluxo de negocio dos scripts",
        ],
        "dependencias": [],
        "saidas": ["scripts param() reutilizaveis com ErrorActionPreference Stop"],
    },
    "domains/languages/fastapi-specialist": {
        "camada": "ferramenta",
        "escopo_negativo": [
            "nao modela migrations de banco (alembic-db-specialist)",
            "nao especializa por empresa (skill de atividade da cadeia)",
        ],
        "dependencias": ["python-specialist"],
        "saidas": ["routers/services FastAPI com testes"],
    },
    "domains/languages/alembic-db-specialist": {
        "camada": "ferramenta",
        "escopo_negativo": [
            "nao decide regra de negocio dos dados",
            "nao roda migration destrutiva sem plano aprovado",
        ],
        "dependencias": ["python-specialist"],
        "saidas": ["migrations versionadas e reversiveis"],
    },
    "domains/languages/redshift-sql-specialist": {
        "camada": "ferramenta",
        "escopo_negativo": [
            "nao aplica regra especifica de empresa (skill de atividade da cadeia)",
            "nao compara regras entre queries (redshift-query-rules-comparator)",
        ],
        "dependencias": [],
        "saidas": ["SQL Redshift otimizado e parametrizado"],
    },
    "domains/tools/postgresql-support": {
        "camada": "ferramenta",
        "escopo_negativo": [
            "nao decide o schema da aplicacao (donas do dominio)",
            "nao substitui migrations (alembic-db-specialist)",
        ],
        "dependencias": [],
        "saidas": ["diagnosticos e queries PostgreSQL parametrizadas"],
    },
    "domains/languages/excel-validation-specialist": {
        "camada": "ferramenta",
        "escopo_negativo": [
            "nao define a regra de negocio das planilhas (skill de atividade)",
        ],
        "dependencias": ["python-specialist"],
        "saidas": ["validadores de planilha parametrizados"],
    },
    "domains/disciplines/databricks-notebook-pattern": {
        "camada": "padroes",
        "escopo_negativo": [
            "nao constroi pipeline de negocio completo (skill de atividade)",
            "nao administra o workspace Databricks",
        ],
        "dependencias": ["python-specialist"],
        "saidas": ["notebooks no padrao com celulas parametrizadas"],
    },
}


def yaml_lista(nome, itens, indent="  "):
    if not itens:
        return ""
    out = f"{indent}{nome}:\n"
    for i in itens:
        out += f"{indent}  - {i}\n"
    return out


def inserir_manifesto(texto, m):
    """Insere campos do manifesto dentro de metadata no frontmatter."""
    fim_fm = texto.index("---", 3)  # fecha frontmatter
    fm = texto[:fim_fm]
    bloco = f"  camada: {m['camada']}\n"
    bloco += yaml_lista("escopo_negativo", m["escopo_negativo"])
    bloco += yaml_lista("dependencias", m["dependencias"])
    bloco += yaml_lista("saidas", m["saidas"])
    if re.search(r"(?m)^metadata:\s*$", fm):
        # metadata existe (triggers): insere logo apos a linha metadata:
        novo = re.sub(r"(?m)^(metadata:\s*)$", r"\1\n" + bloco.rstrip("\n"), fm, count=1)
        # remove linha em branco dupla eventual
        novo = novo.replace("metadata: \n", "metadata:\n")
        return novo + texto[fim_fm:]
    # sem metadata: cria antes do fechamento
    return fm + "metadata:\n" + bloco + texto[fim_fm:]


def adicionar_fallback(texto):
    if "devolver ao `route-skills-by-context`" in texto:
        return texto
    m = re.search(r"(?ms)^## Limites\s*\n(.*?)(?=^## |\Z)", texto)
    if not m:
        return texto
    secao = m.group(1)
    nums = re.findall(r"(?m)^(\d+)\.", secao)
    prox = (max(int(n) for n in nums) + 1) if nums else 1
    # insere apos o ultimo item numerado da secao
    linhas = secao.rstrip("\n").split("\n")
    linhas.append(f"{prox}. {FALLBACK}")
    nova = "\n".join(linhas) + "\n\n"
    return texto[: m.start(1)] + nova + texto[m.end(1):]


alterados = []
for rel, m in LOTE.items():
    p = ROOT / rel / "SKILL.md"
    if not p.exists():
        print(f"FALTA: {rel}")
        continue
    s = io.open(p, encoding="utf-8").read()
    if re.search(r"(?m)^\s+camada:", s):
        print(f"ja tem: {rel}")
        continue
    s = inserir_manifesto(s, m)
    s = adicionar_fallback(s)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    alterados.append(rel)

print(f"\n{len(alterados)} skills populadas:")
for a in alterados:
    print(" -", a)
