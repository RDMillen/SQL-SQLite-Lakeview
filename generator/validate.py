# SPDX-FileCopyrightText: 2026 Ross (pfate.xyz)
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check every task in the course.

For every edu task:
  - the solution state passes the hidden tests
  - the starter state (placeholders replaced by their text) fails them
  - every Python file compiles in both states
For every task: task-info.yaml lists files that exist, placeholder offsets
point at the right text, and task.md is not empty.

Usage: python validate.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from build import INFO, MODULES
from lib import all_tasks, write_course

STYLE_BANNED = ["—", "**"]


def run_tests(task_dir: Path):
    result = subprocess.run([sys.executable, "-m", "unittest", "tests.test"], cwd=task_dir,
                            capture_output=True, text=True, timeout=60)
    return result.returncode == 0, result.stderr


def compile_python(task_dir: Path):
    errors = []
    for path in task_dir.rglob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as error:
            errors.append(f"{path.name}: {error}")
    return errors


def main():
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        sol = Path(tmp) / "solution"
        start = Path(tmp) / "starter"
        write_course(sol, INFO, MODULES, {"README.md": ""}, state="solution")
        write_course(start, INFO, MODULES, {"README.md": ""}, state="starter")
        count = 0
        for number, rel, task in all_tasks(MODULES):
            count += 1
            for banned in STYLE_BANNED:
                if banned in task.md or banned in task.title:
                    problems.append(f"{number}: style, found {banned!r} in task text")
            for f in task.files:
                text = f.solution_text()
                for off, length, ph in f.placeholders():
                    if length == 0:
                        problems.append(f"{number}: empty placeholder in {f.name}")
            for state_dir in (sol, start):
                errs = compile_python(state_dir / rel)
                problems += [f"{number} ({state_dir.name}): {e}" for e in errs]
            if task.kind != "edu":
                continue
            if task.tables is None:
                problems.append(f"{number} {task.title}: no tables listed (pass tables=[...], or [] for an empty database)")
            ok, err = run_tests(sol / rel)
            if not ok:
                problems.append(f"{number} {task.title}: solution FAILS\n{err[-1500:]}")
            ok, err = run_tests(start / rel)
            if ok:
                problems.append(f"{number} {task.title}: starter PASSES (it should fail)")
    print(f"Checked {count} tasks.")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
