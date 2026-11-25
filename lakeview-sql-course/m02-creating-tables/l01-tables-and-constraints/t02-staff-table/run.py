"""Run task.sql and show what it does.

You do not need to change this file. Right-click it and choose Run, or open
it and press the green arrow. Each run starts again from a fresh copy of the
empty database, so you can run it as often as you like.

The run also saves the result as practice.db in this folder. You can open
practice.db in PyCharm's Database tool window to look around.
"""

import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQL_FILE = "task.sql"
LOAD_LAKEVIEW = False


def split_sql(sql):
    statements, current = [], ""
    for ch in sql:
        current += ch
        if ch == ";" and sqlite3.complete_statement(current):
            statements.append(current)
            current = ""
    statements.append(current)
    return [s.strip() for s in statements if strip_comments(s).strip()]


def strip_comments(sql):
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    return re.sub(r"--[^\n]*", " ", sql)


def show(columns, rows):
    cells = [[("NULL" if v is None else str(v)) for v in row] for row in rows]
    widths = [len(c) for c in columns]
    for row in cells:
        widths = [max(w, len(v)) for w, v in zip(widths, row)]
    line = " | ".join(c.ljust(w) for c, w in zip(columns, widths))
    print(line)
    print("-+-".join("-" * w for w in widths))
    for row in cells:
        print(" | ".join(v.ljust(w) for v, w in zip(row, widths)))
    print(f"({len(rows)} row{'' if len(rows) == 1 else 's'})")


def open_database():
    path = HERE / "practice.db"
    try:
        if path.exists():
            path.unlink()
        return sqlite3.connect(path, isolation_level=None)
    except OSError:
        print("practice.db is in use, so this run uses a database in memory.")
        print("Close practice.db in the Database tool window to refresh it.\n")
        return sqlite3.connect(":memory:", isolation_level=None)


def main():
    conn = open_database()
    conn.execute("PRAGMA foreign_keys = ON")
    if LOAD_LAKEVIEW:
        conn.executescript((HERE / "lakeview.sql").read_text(encoding="utf-8"))
    statements = split_sql((HERE / SQL_FILE).read_text(encoding="utf-8"))
    if not statements:
        print(f"{SQL_FILE} has no SQL in it yet.")
        return
    ddl = []
    for number, statement in enumerate(statements, 1):
        print(f"Statement {number}:")
        shown = re.sub(r"^(\s*--[^\n]*\n)+", "", statement).strip()
        print("    " + shown.replace("\n", "\n    "))
        try:
            cursor = conn.execute(statement)
        except sqlite3.Error as error:
            print(f"\nError: {error}")
            return
        if cursor.description:
            show([d[0] for d in cursor.description], cursor.fetchall())
        elif cursor.rowcount >= 0:
            print(f"OK. Rows changed: {cursor.rowcount}")
        else:
            print("OK.")
        if re.match(r"\s*(CREATE|ALTER|DROP)\b", strip_comments(statement), re.I):
            ddl.append(statement)
        print()
    if ddl:
        print("Tables changed by your SQL:")
        for name, sql in conn.execute(
                "SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name"):
            if any(re.search(r"\b" + re.escape(name) + r"\b", s, re.I) for s in ddl):
                print(sql)
                print()


if __name__ == "__main__":
    main()
