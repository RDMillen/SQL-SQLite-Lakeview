# SPDX-FileCopyrightText: 2026 Ross (pfate.xyz)
# SPDX-License-Identifier: GPL-3.0-or-later
"""Course model and writer for the SQL with SQLite course.

Every task is described in Python (see the mNN_*.py files) and written out
as a JetBrains Academy course folder by build.py.

Files that hold placeholders are written as a list of parts. A plain string
is fixed text. A P(solution, placeholder) part is a placeholder: the course
file holds the solution (creator mode) and the learner sees the placeholder
text.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class P:
    solution: str
    placeholder: str


def q(text: str) -> str:
    """Quote a string for YAML. JSON strings are valid YAML scalars."""
    return json.dumps(text, ensure_ascii=False)


@dataclass
class TaskFile:
    name: str
    parts: list  # list of str or P
    visible: bool = True
    editable: bool = True
    propagatable: bool | None = None

    def solution_text(self) -> str:
        return "".join(p.solution if isinstance(p, P) else p for p in self.parts)

    def starter_text(self) -> str:
        return "".join(p.placeholder if isinstance(p, P) else p for p in self.parts)

    def placeholders(self):
        """Yield (offset, length, placeholder_text) in solution coordinates."""
        offset = 0
        for p in self.parts:
            if isinstance(p, P):
                yield offset, len(p.solution), p.placeholder
                offset += len(p.solution)
            else:
                offset += len(p)


def fixed(name: str, text: str, **kw) -> TaskFile:
    return TaskFile(name, [text], **kw)


@dataclass
class Task:
    slug: str
    title: str          # without the number, e.g. "Your first SELECT"
    kind: str           # edu | theory | choice
    md: str
    files: list = field(default_factory=list)
    # choice tasks
    options: list = field(default_factory=list)   # list of (text, is_correct)
    multiple: bool = False
    message_incorrect: str = "Not quite. Read the question again and try once more."
    message_correct: str = "Correct."
    # tables the task uses; None means not set (the validator reports it)
    tables: list | None = None


@dataclass
class Lesson:
    slug: str
    title: str
    tasks: list


@dataclass
class Module:
    slug: str
    title: str
    lessons: list


# ----------------------------------------------------------------- writing

def _task_yaml(task: Task, number: str) -> str:
    lines = [f"type: {task.kind}", f"custom_name: {q(number + ' ' + task.title)}"]
    if task.kind == "choice":
        lines.append(f"is_multiple_choice: {'true' if task.multiple else 'false'}")
        lines.append("options:")
        for text, ok in task.options:
            lines.append(f"  - text: {q(text)}")
            lines.append(f"    is_correct: {'true' if ok else 'false'}")
        lines.append(f"message_correct: {q(task.message_correct)}")
        lines.append(f"message_incorrect: {q(task.message_incorrect)}")
        lines.append("local_check: true")
    lines.append("files:")
    for f in task.files:
        lines.append(f"  - name: {f.name}")
        lines.append(f"    visible: {'true' if f.visible else 'false'}")
        phs = list(f.placeholders())
        if phs:
            lines.append("    placeholders:")
            for off, length, text in phs:
                lines.append(f"      - offset: {off}")
                lines.append(f"        length: {length}")
                lines.append(f"        placeholder_text: {q(text)}")
        if not f.editable:
            lines.append("    editable: false")
        if f.propagatable is not None:
            lines.append(f"    propagatable: {'true' if f.propagatable else 'false'}")
    return "\n".join(lines) + "\n"


def _content_yaml(title: str, children: list, extra: str = "") -> str:
    out = ""
    if extra:
        out += extra + "\n"
    out += f"custom_name: {q(title)}\ncontent:\n"
    out += "".join(f"  - {c}\n" for c in children)
    return out


def write_course(root: Path, info: dict, modules: list, additional: dict, state: str = "solution"):
    """Write the course. state is 'solution' (creator mode) or 'starter'."""
    root.mkdir(parents=True, exist_ok=True)
    # A Marketplace course: the plugin gives every item an id and stores it in a
    # *-remote-info.yaml file next to its config. build.py keeps those files when it
    # rebuilds, so commit them to Git. Marketplace uses the ids to recognise updates.
    course = [
        "type: marketplace",
        f"title: {q(info['title'])}",
        "language: English",
        f"summary: {q(info['summary'])}",
        "programming_language: Python",
        "environment: unittest",
        "content:",
    ]
    course += [f"  - {m.slug}" for m in modules]
    course.append("additional_files:")
    course += [f"  - name: {name}" for name in additional]
    course.append("yaml_version: 6")
    (root / "course-info.yaml").write_text("\n".join(course) + "\n", encoding="utf-8")
    for name, text in additional.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text, encoding="utf-8")

    for mi, m in enumerate(modules, 1):
        mdir = root / m.slug
        mdir.mkdir(exist_ok=True)
        (mdir / "section-info.yaml").write_text(
            _content_yaml(f"Module {mi}: {m.title}", [l.slug for l in m.lessons]), encoding="utf-8")
        for li, lesson in enumerate(m.lessons, 1):
            ldir = mdir / lesson.slug
            ldir.mkdir(exist_ok=True)
            (ldir / "lesson-info.yaml").write_text(
                _content_yaml(f"{mi}.{li} {lesson.title}", [t.slug for t in lesson.tasks]), encoding="utf-8")
            for ti, task in enumerate(lesson.tasks, 1):
                tdir = ldir / task.slug
                tdir.mkdir(exist_ok=True)
                number = f"{mi}.{li}.{ti}"
                (tdir / "task-info.yaml").write_text(_task_yaml(task, number), encoding="utf-8")
                (tdir / "task.md").write_text(task.md.strip() + "\n", encoding="utf-8")
                for f in task.files:
                    path = tdir / f.name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    text = f.solution_text() if state == "solution" else f.starter_text()
                    path.write_text(text, encoding="utf-8")


def all_tasks(modules):
    for mi, m in enumerate(modules, 1):
        for li, lesson in enumerate(m.lessons, 1):
            for ti, task in enumerate(lesson.tasks, 1):
                yield f"{mi}.{li}.{ti}", f"{m.slug}/{lesson.slug}/{task.slug}", task
