"""Shared files and task builders for the SQL with SQLite course."""

from textwrap import dedent

from lib import P, Task, TaskFile, fixed

# --------------------------------------------------------------- database

LAKEVIEW_SQL = """\
-- Lakeview Hotel drill database
-- This file builds the database used in every task. It is locked so that
-- everyone works with the same data. Read it to see the tables and rows.
--
-- The real Lakeview booking site stores Werkzeug password hashes. These
-- rows use 'demo-hash' because the drills never log anyone in.

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    number INTEGER NOT NULL UNIQUE,
    room_type TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    price_per_night REAL NOT NULL CHECK (price_per_night > 0),
    available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    check_in TEXT NOT NULL,
    check_out TEXT NOT NULL,
    occupants INTEGER NOT NULL CHECK (occupants > 0),
    total_price REAL NOT NULL
);

CREATE TABLE extras (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE booking_extras (
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    extra_id INTEGER NOT NULL REFERENCES extras(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (booking_id, extra_id)
);

INSERT INTO users (id, name, email, password_hash, phone) VALUES
    (1, 'James Sunderland', 'james@example.com', 'demo-hash', '07700 900001'),
    (2, 'Mary Sunderland', 'mary@example.com', 'demo-hash', '07700 900002'),
    (3, 'Harry Mason', 'harry@example.com', 'demo-hash', NULL),
    (4, 'Heather Mason', 'heather@example.com', 'demo-hash', '07700 900004'),
    (5, 'Henry Townshend', 'henry@example.com', 'demo-hash', NULL),
    (6, 'Eileen Galvin', 'eileen@example.com', 'demo-hash', NULL);

INSERT INTO rooms (id, number, room_type, capacity, price_per_night, available) VALUES
    (1, 101, 'Single', 1, 80.0, 1),
    (2, 102, 'Double', 2, 120.0, 0),
    (3, 103, 'Double', 2, 110.0, 1),
    (4, 201, 'Family', 4, 180.0, 1),
    (5, 312, 'Suite', 3, 250.0, 1);

-- Price rule: the nightly rate covers 2 guests, and each guest above 2
-- adds 10 per night.
INSERT INTO bookings (id, user_id, room_id, check_in, check_out, occupants, total_price) VALUES
    (1, 1, 1, '2026-11-01', '2026-11-04', 1, 240.0),
    (2, 2, 4, '2026-11-10', '2026-11-12', 3, 380.0),
    (3, 1, 1, '2026-12-01', '2026-12-03', 1, 160.0),
    (4, 3, 5, '2026-11-20', '2026-11-23', 2, 750.0),
    (5, 4, 3, '2026-11-04', '2026-11-06', 2, 220.0),
    (6, 5, 4, '2026-12-20', '2026-12-27', 4, 1400.0),
    (7, 2, 5, '2026-12-24', '2026-12-26', 3, 520.0),
    (8, 3, 3, '2026-12-01', '2026-12-02', 1, 110.0),
    (9, 4, 1, '2026-11-04', '2026-11-07', 1, 240.0),
    (10, 5, 5, '2027-01-02', '2027-01-05', 3, 780.0);

INSERT INTO extras (id, name, price) VALUES
    (1, 'Breakfast', 12.5),
    (2, 'Parking', 8.0),
    (3, 'Late checkout', 25.0),
    (4, 'Boat hire', 40.0);

INSERT INTO booking_extras (booking_id, extra_id, quantity) VALUES
    (1, 1, 3),
    (1, 2, 3),
    (2, 1, 6),
    (4, 1, 6),
    (4, 3, 1),
    (6, 1, 28),
    (6, 2, 7),
    (7, 3, 1),
    (9, 1, 3),
    (10, 2, 3);
"""

# Extra rows the hidden tests add on a second run, so that an answer which
# types out the expected rows by hand does not pass.
EXTRA_SQL = """\
INSERT INTO users (id, name, email, password_hash, phone) VALUES
    (7, 'Cybil Bennett', 'cybil@example.com', 'demo-hash', NULL),
    (8, 'Douglas Cartland', 'douglas@example.com', 'demo-hash', '07700 900008');
INSERT INTO rooms (id, number, room_type, capacity, price_per_night, available) VALUES
    (6, 202, 'Double', 2, 130.0, 1),
    (7, 104, 'Single', 1, 75.0, 1);
INSERT INTO bookings (id, user_id, room_id, check_in, check_out, occupants, total_price) VALUES
    (11, 7, 6, '2026-11-15', '2026-11-18', 2, 390.0),
    (12, 8, 5, '2026-11-02', '2026-11-04', 3, 520.0),
    (13, 7, 1, '2026-12-02', '2026-12-05', 1, 240.0);
INSERT INTO booking_extras (booking_id, extra_id, quantity) VALUES
    (11, 1, 6),
    (12, 4, 1),
    (13, 2, 3);
"""

# --------------------------------------------------------------- run.py

RUN_PY = '''\
"""Run {sql_file} and show what it does.

You do not need to change this file. Right-click it and choose Run, or open
it and press the green arrow. Each run starts again from a fresh copy of the
{base}, so you can run it as often as you like.

The run also saves the result as practice.db in this folder. You can open
practice.db in PyCharm's Database tool window to look around.
"""

import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQL_FILE = "{sql_file}"
LOAD_LAKEVIEW = {load}


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
    sql = re.sub(r"/\\*.*?\\*/", " ", sql, flags=re.S)
    return re.sub(r"--[^\\n]*", " ", sql)


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
    print(f"({{len(rows)}} row{{'' if len(rows) == 1 else 's'}})")


def open_database():
    path = HERE / "practice.db"
    try:
        if path.exists():
            path.unlink()
        return sqlite3.connect(path, isolation_level=None)
    except OSError:
        print("practice.db is in use, so this run uses a database in memory.")
        print("Close practice.db in the Database tool window to refresh it.\\n")
        return sqlite3.connect(":memory:", isolation_level=None)


def main():
    conn = open_database()
    conn.execute("PRAGMA foreign_keys = ON")
    if LOAD_LAKEVIEW:
        conn.executescript((HERE / "lakeview.sql").read_text(encoding="utf-8"))
    statements = split_sql((HERE / SQL_FILE).read_text(encoding="utf-8"))
    if not statements:
        print(f"{{SQL_FILE}} has no SQL in it yet.")
        return
    ddl = []
    for number, statement in enumerate(statements, 1):
        print(f"Statement {{number}}:")
        shown = re.sub(r"^(\\s*--[^\\n]*\\n)+", "", statement).strip()
        print("    " + shown.replace("\\n", "\\n    "))
        try:
            cursor = conn.execute(statement)
        except sqlite3.Error as error:
            print(f"\\nError: {{error}}")
            return
        if cursor.description:
            show([d[0] for d in cursor.description], cursor.fetchall())
        elif cursor.rowcount >= 0:
            print(f"OK. Rows changed: {{cursor.rowcount}}")
        else:
            print("OK.")
        if re.match(r"\\s*(CREATE|ALTER|DROP)\\b", strip_comments(statement), re.I):
            ddl.append(statement)
        print()
    if ddl:
        print("Tables changed by your SQL:")
        for name, sql in conn.execute(
                "SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name"):
            if any(re.search(r"\\b" + re.escape(name) + r"\\b", s, re.I) for s in ddl):
                print(sql)
                print()


if __name__ == "__main__":
    main()
'''


def run_py(sql_file="task.sql", lakeview=True):
    base = "Lakeview database" if lakeview else "empty database"
    return RUN_PY.format(sql_file=sql_file, load="True" if lakeview else "False", base=base)


# --------------------------------------------------------------- tests

TEST_PREAMBLE = '''\
# Hidden tests for this task. Shared helpers first, then the checks.
import importlib
import inspect
import re
import sqlite3
import sys
import unittest
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent.parent
if str(TASK_DIR) not in sys.path:
    sys.path.insert(0, str(TASK_DIR))


def read(name):
    return (TASK_DIR / name).read_text(encoding="utf-8")


def strip_comments(sql):
    sql = re.sub(r"/\\*.*?\\*/", " ", sql, flags=re.S)
    return re.sub(r"--[^\\n]*", " ", sql)


def split_sql(sql):
    statements, current = [], ""
    for ch in sql:
        current += ch
        if ch == ";" and sqlite3.complete_statement(current):
            statements.append(current)
            current = ""
    statements.append(current)
    return [s.strip() for s in statements if strip_comments(s).strip()]


EXTRA_SQL = """{extra}"""


def new_db(lakeview=True, extra=False):
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.execute("PRAGMA foreign_keys = ON")
    if lakeview:
        conn.executescript(read("lakeview.sql"))
    if extra:
        conn.executescript(EXTRA_SQL)
    return conn


def norm(value):
    return round(value, 2) if isinstance(value, float) else value


def sort_key(row):
    return tuple((0, "") if v is None else (1, v) if isinstance(v, (int, float)) else (2, str(v))
                 for v in row)


def show_row(row):
    return "(" + ", ".join("NULL" if v is None else repr(v) for v in row) + ")"


class SQLTestCase(unittest.TestCase):
    maxDiff = None
    longMessage = False
    MUST_USE = ()
    MUST_NOT_USE = ()

    def student_sql(self, name="task.sql"):
        sql = read(name)
        statements = split_sql(sql)
        if not statements:
            self.fail(f"{{name}} has no SQL in it yet. Write your SQL below the comments.")
        return sql, statements

    def run_sql(self, conn, statements, where=""):
        results = []
        for statement in statements:
            try:
                cursor = conn.execute(statement)
            except sqlite3.Error as error:
                self.fail(f"{{where}}Your SQL gave an error: {{error}}\\nThe statement was:\\n{{statement}}")
            columns = [d[0] for d in cursor.description] if cursor.description else None
            rows = cursor.fetchall() if columns is not None else None
            results.append((statement, columns, rows))
        return results

    def last_select(self, results):
        for _, columns, rows in reversed(results):
            if columns is not None:
                return columns, rows
        self.fail("Your SQL does not return any rows. This task needs a SELECT statement.")

    def compare(self, got_cols, got, exp_cols, exp, ordered=False, names=False, where=""):
        if len(got_cols) != len(exp_cols):
            self.fail(f"{{where}}Your query returns {{len(got_cols)}} column(s), but it should return "
                      f"{{len(exp_cols)}}. Check the list of columns after SELECT.")
        if names:
            for g, e in zip(got_cols, exp_cols):
                if g.lower() != e.lower():
                    self.fail(f"{{where}}A column should be called {{e}}, but yours is called {{g}}. "
                              f"Use AS to name it.")
        got = [tuple(norm(v) for v in r) for r in got]
        exp = [tuple(norm(v) for v in r) for r in exp]
        if len(got) != len(exp):
            self.fail(f"{{where}}Your query returned {{len(got)}} row(s), but it should return {{len(exp)}}.")
        remaining = list(got)
        missing = []
        for row in exp:
            if row in remaining:
                remaining.remove(row)
            else:
                missing.append(row)
        if missing:
            self.fail(f"{{where}}The rows are not right.\\nThis row is missing: {{show_row(missing[0])}}\\n"
                      f"This row should not be there: {{show_row(remaining[0])}}")
        if ordered and got != exp:
            self.fail(f"{{where}}The rows are right, but they are in the wrong order. Check your ORDER BY.")

    def check_keywords(self, sql):
        clean = strip_comments(sql)
        for word in self.MUST_USE:
            if not re.search(r"\\b" + re.escape(word).replace("\\\\ ", "\\\\s+") + r"\\b", clean, re.I):
                self.fail(f"Your SQL should use {{word}} for this task.")
        for word in self.MUST_NOT_USE:
            if re.search(r"\\b" + re.escape(word).replace("\\\\ ", "\\\\s+") + r"\\b", clean, re.I):
                self.fail(f"Do not use {{word}} in this task.")

    def expect_error(self, conn, sql, message):
        try:
            conn.execute(sql)
        except sqlite3.Error:
            return
        self.fail(message)

    def expect_ok(self, conn, sql, message):
        try:
            conn.execute(sql)
        except sqlite3.Error as error:
            self.fail(f"{{message}} SQLite said: {{error}}")


def columns_of(conn, table):
    """Map column name to (type, notnull, default, pk position)."""
    return {{row[1].lower(): (row[2].upper(), row[3], row[4], row[5])
            for row in conn.execute(f"PRAGMA table_info({{table}})")}}


def foreign_keys_of(conn, table):
    """List of (from column, to table, to column, on delete)."""
    return [(row[3].lower(), row[2].lower(), (row[4] or "").lower(), row[6].upper())
            for row in conn.execute(f"PRAGMA foreign_key_list({{table}})")]


def table_exists(conn, table):
    return conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ? COLLATE NOCASE",
                        (table,)).fetchone() is not None

'''


def preamble():
    return TEST_PREAMBLE.format(extra=EXTRA_SQL)


SELECT_TESTS = '''
REFERENCE = """{reference}"""


class TestTask(SQLTestCase):
    MUST_USE = {must_use!r}
    MUST_NOT_USE = {must_not_use!r}

    def check(self, extra):
        where = "With some extra rows added to the database: " if extra else ""
        sql, statements = self.student_sql()
        columns, rows = self.last_select(self.run_sql(new_db(extra=extra), statements, where))
        ref = new_db(extra=extra).execute(REFERENCE)
        self.compare(columns, rows, [d[0] for d in ref.description], ref.fetchall(),
                     ordered={ordered}, names={names}, where=where)

    def test_1_query(self):
        self.check(False)

    def test_2_more_data(self):
        self.check({extra})

    def test_3_keywords(self):
        sql, _ = self.student_sql()
        self.check_keywords(sql)
'''

STATE_TESTS = '''
REFERENCE = """{reference}"""

PROBES = {probes!r}


class TestTask(SQLTestCase):
    MUST_USE = {must_use!r}
    MUST_NOT_USE = {must_not_use!r}

    def check(self, extra):
        where = "With some extra rows added to the database: " if extra else ""
        sql, statements = self.student_sql()
        conn = new_db(lakeview={lakeview}, extra=extra)
        self.run_sql(conn, statements, where)
        ref = new_db(lakeview={lakeview}, extra=extra)
        ref.executescript(REFERENCE)
        for probe, label in PROBES:
            got = conn.execute(probe)
            exp = ref.execute(probe)
            self.compare([d[0] for d in got.description], got.fetchall(),
                         [d[0] for d in exp.description], exp.fetchall(), ordered=True,
                         where=f"{{where}}After your SQL runs, {{label}} is not right. ")

    def test_1_changes(self):
        self.check(False)

    def test_2_more_data(self):
        self.check({extra})

    def test_3_keywords(self):
        sql, _ = self.student_sql()
        self.check_keywords(sql)
'''


# --------------------------------------------------------------- builders

# Columns of each Lakeview table, with the table and column a foreign key links to.
SCHEMA = {
    "users": ["id", "name", "email", "password_hash", "phone"],
    "rooms": ["id", "number", "room_type", "capacity", "price_per_night", "available"],
    "bookings": ["id", ("user_id", "users.id"), ("room_id", "rooms.id"), "check_in", "check_out",
                 "occupants", "total_price"],
    "extras": ["id", "name", "price"],
    "booking_extras": [("booking_id", "bookings.id"), ("extra_id", "extras.id"), "quantity"],
}


def tables_md(tables):
    if not tables:
        return ""
    lines = ["", "## Tables you need", ""]
    for table in tables:
        cols = [f"`{c[0]}` (links to `{c[1]}`)" if isinstance(c, tuple) else f"`{c}`" for c in SCHEMA[table]]
        lines.append(f"- `{table}`: " + ", ".join(cols))
    lines += ["", "Open `lakeview.sql` to see every row."]
    return "\n".join(lines) + "\n"


def tables_header(tables):
    if not tables:
        return []
    lines = ["", "Tables you need:"]
    for table in tables:
        cols = [f"{c[0]} (links to {c[1]})" if isinstance(c, tuple) else c for c in SCHEMA[table]]
        lines.append(f"  {table}: " + ", ".join(cols))
    return lines

def _md(text):
    return dedent(text).strip() + "\n"


def _sql_header(lines):
    return "".join(f"-- {line}\n" if line else "--\n" for line in lines) + "\n"


def _common_files(lakeview=True, sql_file="task.sql"):
    return [
        fixed("lakeview.sql", LAKEVIEW_SQL, editable=False),
        fixed("run.py", run_py(sql_file, lakeview), editable=False),
    ]


def _test_files(code):
    return [
        fixed("tests/test.py", preamble() + code, visible=False),
        fixed("tests/__init__.py", "", visible=False, propagatable=False),
    ]


def theory(slug, title, md, examples=None, lakeview=True):
    files = []
    if examples:
        files.append(fixed("examples.sql", dedent(examples).strip() + "\n"))
        files += _common_files(lakeview, "examples.sql")
    else:
        files.append(fixed("lakeview.sql", LAKEVIEW_SQL, editable=False))
    return Task(slug, title, "theory", _md(md), files)


def choice(slug, title, md, options, correct, multiple=False, incorrect=None, correct_msg=None):
    task = Task(slug, title, "choice", _md(md),
                [fixed("lakeview.sql", LAKEVIEW_SQL, editable=False)],
                options=[(o, i in correct) for i, o in enumerate(options)], multiple=multiple)
    if incorrect:
        task.message_incorrect = incorrect
    if correct_msg:
        task.message_correct = correct_msg
    return task


def _parts_solution(sql_parts):
    return "".join(p.solution if isinstance(p, P) else p for p in sql_parts)


def _task_sql(header, sql_parts, solution, placeholder, tables=None):
    header = list(header) + tables_header(tables)
    if sql_parts is None:
        sql_parts = [P(dedent(solution).strip(), dedent(placeholder).strip())]
    return TaskFile("task.sql", [_sql_header(header)] + sql_parts + ["\n"])


def select_task(slug, title, md, header, solution, placeholder="-- Write your query here",
                reference=None, ordered=False, names=False, must_use=(), must_not_use=(),
                extra=True, sql_parts=None, tables=None):
    reference = dedent(reference or solution or _parts_solution(sql_parts)).strip()
    code = SELECT_TESTS.format(reference=reference, must_use=tuple(must_use),
                               must_not_use=tuple(must_not_use), ordered=ordered,
                               names=names, extra=extra)
    files = [_task_sql(header, sql_parts, solution, placeholder, tables)] + _common_files() + _test_files(code)
    return Task(slug, title, "edu", _md(md) + tables_md(tables), files, tables=tables)


def state_task(slug, title, md, header, solution, probes, placeholder="-- Write your SQL here",
               reference=None, must_use=(), must_not_use=(), lakeview=True, extra=True,
               sql_parts=None, tables=None):
    reference = dedent(reference or solution or _parts_solution(sql_parts)).strip()
    code = STATE_TESTS.format(reference=reference, probes=list(probes), must_use=tuple(must_use),
                              must_not_use=tuple(must_not_use), lakeview=lakeview, extra=extra)
    files = [_task_sql(header, sql_parts, solution, placeholder, tables)] + _common_files(lakeview) + _test_files(code)
    return Task(slug, title, "edu", _md(md) + tables_md(tables), files, tables=tables)


def custom_task(slug, title, md, header, solution, tests, placeholder="-- Write your SQL here",
                lakeview=True, sql_parts=None, tables=None):
    files = [_task_sql(header, sql_parts, solution, placeholder, tables)] + _common_files(lakeview)
    files += _test_files(dedent(tests))
    return Task(slug, title, "edu", _md(md) + tables_md(tables), files, tables=tables)


def py_task(slug, title, md, module_name, parts, tests, tables=None):
    files = [
        TaskFile(module_name, parts),
        fixed("lakeview.sql", LAKEVIEW_SQL, editable=False),
    ]
    files += _test_files(dedent(tests))
    return Task(slug, title, "edu", _md(md) + tables_md(tables), files, tables=tables)
