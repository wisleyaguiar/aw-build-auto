#!/usr/bin/env python3
"""Portão do Protocolo 0 (V.L.A.E.G.).

Hook PreToolUse: bloqueia escrita em tools/ até os 3 portões estarem marcados no task_plan.md.
Exit 0 libera; exit 2 bloqueia e o stderr volta para o Claude.
shortcut: só vê Write/Edit/MultiEdit, não escrita via Bash; é trava de processo, não de segurança.
"""
import json
import os
import re
import sys
from pathlib import Path

# Copiados byte a byte em skills/piloto/templates/task_plan.md e skills/piloto/SKILL.md.
GATES = (
    "Descoberta respondida",
    "Esquema de Dados confirmado no CLAUDE.md",
    "Blueprint aprovado",
)
SECTION = "## Portões"


def find_root(path):
    for parent in path.parents:
        if (parent / "task_plan.md").is_file():
            return parent
    return None


def missing_gates(plan):
    return [g for g in GATES if not re.search(r"^- \[[xX]\] " + re.escape(g) + r"\s*$", plan, re.M)]


def main():
    data = json.load(sys.stdin)
    file_path = (data.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    path = Path(os.path.normpath(Path(data.get("cwd") or os.getcwd()) / file_path))
    root = find_root(path)
    if root is None:
        return 0
    plan = (root / "task_plan.md").read_text(encoding="utf-8")
    if SECTION not in plan or path.relative_to(root).parts[:1] != ("tools",):
        return 0
    missing = missing_gates(plan)
    if not missing:
        return 0
    print(
        "V.L.A.E.G. Protocolo 0: proibido escrever em tools/ antes dos portões. "
        f"Faltam no {root / 'task_plan.md'}: " + "; ".join(f"- [x] {g}" for g in missing) + ". "
        "Termine a Fase V e marque cada portão só depois do OK explícito do usuário. "
        "Não contorne este bloqueio via Bash.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
