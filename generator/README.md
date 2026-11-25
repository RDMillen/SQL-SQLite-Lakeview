# SQL with SQLite - The Lakeview Hotel: course generator

These scripts write the JetBrains Academy course folder for SQL with SQLite - The Lakeview Hotel.
Keep them with the course: the course folder is generated from them, so
edit the scripts and rebuild instead of editing the course by hand.

| File | What it holds |
|---|---|
| `lib.py` | The course model (modules, lessons, tasks, placeholders) and the YAML writer |
| `shared.py` | `lakeview.sql`, the extra test rows, `run.py`, the hidden test helpers, and the task builders |
| `m01_reading.py` to `m08_errors.py` | One file per module, holding the task text, solutions, and tests |
| `build.py` | Writes the course folder, with `README.md`, `LICENSE`, and `.courseignore` |
| `LICENSE-CC-BY-SA-4.0.txt` | The licence text copied into the course |
| `validate.py` | Checks every task |

## Build and check

```
python build.py
python validate.py
```

`build.py` writes to `../lakeview-sql-course`, next to this folder. Give it a
path to write somewhere else.

`validate.py` builds the course twice, once as the solution and once as the
starter (every placeholder replaced by its placeholder text). For each edu
task it checks that the solution passes the hidden tests and the starter
fails them. It also compiles every Python file in both states and looks for
em dashes and bold in task text.

## Task builders

- `select_task`: the student writes a SELECT. The tests compare its rows with
  the reference query, on the seed data and again with `EXTRA_SQL` added.
- `state_task`: the student changes data or tables. The tests run the student
  SQL and the reference SQL on two fresh databases, then compare the probe
  queries.
- `custom_task`: hand-written tests, used for CREATE TABLE tasks, where the
  tests check behaviour (inserts that should pass or fail) and PRAGMA output.
- `py_task`: a Python file with placeholders and hand-written tests.
- `theory` and `choice`: reading tasks and quizzes.

Placeholders are written as `P(solution, placeholder_text)` inside a list of
file parts. Offsets in `task-info.yaml` are worked out by the writer.

## Marketplace ids

The course is a Marketplace course (`type: marketplace` in
`course-info.yaml`). The first time you archive or upload it, the plugin gives
every module, lesson, and task an id and saves it in a `*-remote-info.yaml`
file beside that item's config. Marketplace uses these ids to match an
updated course to the one students already have.

- Commit the `*-remote-info.yaml` files to Git.
- `build.py` keeps them when it rebuilds the course folder.
- Renaming a module, lesson, or task folder loses its id, so students see it
  as a new item. `build.py` lists any ids it had to drop.
- If the plugin says "YAML remote configuration is broken", an item has an id
  in memory but no file on disk. Close the project, reopen the folder, and try
  again.

## Distributing

Open `lakeview-sql-course` in PyCharm with the JetBrains Academy plugin.

- For a file to share: Create Course Archive. A plain zip of the folder is not
  accepted as a course.
- For Marketplace: use the plugin's upload action, signed in to your
  publishing account.

`.courseignore` keeps `practice.db` (made by `run.py`) and `__pycache__`
out of the archive.
