#!/usr/bin/env python3
"""Self-test do plugin. Rode: python3 -m unittest hooks/test_gate_tools.py"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "gate_tools.py"
SKILL_DIR = HERE.parent / "skills" / "piloto"
sys.path.insert(0, str(HERE))
from gate_tools import GATES  # noqa: E402


def run_gate(file_path, cwd="/"):
    payload = {"tool_name": "Write", "tool_input": {"file_path": str(file_path)}, "cwd": str(cwd)}
    return subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload), capture_output=True, text=True)


def plan(marks):
    return "# Plano\n\n## Portões (Protocolo 0)\n\n" + "".join(f"- [{m}] {g}\n" for m, g in zip(marks, GATES))


class GateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_plan(self, text):
        (self.root / "task_plan.md").write_text(text, encoding="utf-8")

    def test_outside_tools_allows(self):
        self.write_plan(plan("   "))
        self.assertEqual(run_gate(self.root / "src" / "app.py").returncode, 0)

    def test_no_task_plan_allows(self):
        self.assertEqual(run_gate(self.root / "tools" / "x.py").returncode, 0)

    def test_plan_without_gates_section_allows(self):
        self.write_plan("# Outro plano\n")
        self.assertEqual(run_gate(self.root / "tools" / "x.py").returncode, 0)

    def test_open_gates_block(self):
        self.write_plan(plan("   "))
        r = run_gate(self.root / "tools" / "x.py")
        self.assertEqual(r.returncode, 2)
        for g in GATES:
            self.assertIn(g, r.stderr)

    def test_one_open_gate_blocks_and_names_it(self):
        self.write_plan(plan("xx "))
        r = run_gate(self.root / "tools" / "x.py")
        self.assertEqual(r.returncode, 2)
        self.assertIn(GATES[2], r.stderr)
        self.assertNotIn(GATES[0], r.stderr)

    def test_closed_gates_allow(self):
        for marks in ("xxx", "XXX", "xXx"):
            self.write_plan(plan(marks))
            self.assertEqual(run_gate(self.root / "tools" / "x.py").returncode, 0, marks)

    def test_nested_tools_dir_allows(self):
        self.write_plan(plan("   "))
        self.assertEqual(run_gate(self.root / "src" / "tools" / "x.py").returncode, 0)

    def test_relative_path_uses_cwd(self):
        self.write_plan(plan("   "))
        self.assertEqual(run_gate("tools/x.py", cwd=self.root).returncode, 2)

    def test_missing_file_path_allows(self):
        r = subprocess.run([sys.executable, str(GATE)], input='{"tool_input": {}}', capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


class TemplateTest(unittest.TestCase):
    def test_gate_texts_match_template_and_skill(self):
        template = (SKILL_DIR / "templates" / "task_plan.md").read_text(encoding="utf-8")
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Portões", template)
        for g in GATES:
            self.assertIn(f"- [ ] {g}\n", template)
            self.assertIn(f"- [x] {g}`", skill)

    def test_handshake_template_fails_cleanly_without_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "tools" / "handshake_servico.py"
            script.parent.mkdir()
            shutil.copy(SKILL_DIR / "templates" / "handshake.py", script)
            env = {k: v for k, v in os.environ.items() if k != "SERVICO_TOKEN"}
            r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FALHA servico: faltam no .env: SERVICO_TOKEN", r.stdout)


if __name__ == "__main__":
    unittest.main()
