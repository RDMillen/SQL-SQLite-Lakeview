"""Build the SQL with SQLite course folder.

Usage: python build.py [output folder]
The default output folder is ../lakeview-sql-course next to this folder.
"""

import shutil
import sys
from pathlib import Path

from lib import write_course
import m01_reading
import m02_creating
import m03_changing
import m04_aggregates
import m05_joins
import m06_dates
import m07_python
import m08_errors

HERE = Path(__file__).resolve().parent

MODULES = [
    m01_reading.MODULE,
    m02_creating.MODULE,
    m03_changing.MODULE,
    m04_aggregates.MODULE,
    m05_joins.MODULE,
    m06_dates.MODULE,
    m07_python.MODULE,
    m08_errors.MODULE,
]

INFO = {
    "title": "SQL with SQLite - The Lakeview Hotel",
    "summary": "SQL drills on the Lakeview Hotel database: reading data, creating tables, "
               "changing data, aggregates, joins, dates and subqueries, SQL from Python, and "
               "reading error messages.",
}

README = """\
# SQL with SQLite - The Lakeview Hotel

SQL practice with SQLite. Every task uses the same small database for the
Lakeview Hotel, on the shore of Toluca Lake.

## What it covers

1. Reading data: SELECT, WHERE, ORDER BY, LIKE, and NULL
2. Creating tables: types, keys, constraints, and foreign keys
3. Changing data: INSERT, UPDATE, DELETE, and transactions
4. Counting and grouping: aggregates, GROUP BY, and HAVING
5. Joining tables: inner joins, LEFT JOIN, and joins across four tables
6. Dates and subqueries: julianday, clash checks, and NOT EXISTS
7. SQL from Python: the sqlite3 module, placeholders, and IntegrityError
8. Reading errors: what SQLite error messages mean

## How to use it

Each task folder has a `task.sql` file for your SQL, a locked `lakeview.sql`
that builds the database, and a locked `run.py` that runs your SQL and shows
the results. Run `run.py` to see what your SQL does, then press Check.

## Licence

This course is licensed under the Creative Commons Attribution-ShareAlike
4.0 International licence (CC BY-SA 4.0). See LICENSE, or
https://creativecommons.org/licenses/by-sa/4.0/
"""


LICENSE = (HERE / "LICENSE-CC-BY-SA-4.0.txt").read_text(encoding="utf-8")

# Files the plugin should leave out of the course archive. Works like .gitignore.
COURSE_IGNORE = """\
practice.db
__pycache__/
*.pyc
.idea/
"""

KEEP = "*-remote-info.yaml"


def build(out: Path):
    # Keep the plugin's Marketplace ids (*-remote-info.yaml) across rebuilds.
    kept = {}
    if out.exists():
        kept = {p.relative_to(out): p.read_bytes() for p in out.rglob(KEEP)}
        shutil.rmtree(out)
    write_course(out, INFO, MODULES, {
        "README.md": README,
        "LICENSE": LICENSE,
        ".courseignore": COURSE_IGNORE,
    })
    orphans = []
    for rel, data in kept.items():
        target = out / rel
        if target.parent.exists():
            target.write_bytes(data)
        else:
            orphans.append(str(rel))
    if kept:
        print(f"Kept {len(kept) - len(orphans)} remote-info file(s).")
    if orphans:
        print("These remote-info files belong to folders that no longer exist, so they were dropped.")
        print("A renamed module, lesson or task becomes a new item on Marketplace:")
        print("\n".join("  " + o for o in orphans))
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "lakeview-sql-course"
    print("Built", build(target))
