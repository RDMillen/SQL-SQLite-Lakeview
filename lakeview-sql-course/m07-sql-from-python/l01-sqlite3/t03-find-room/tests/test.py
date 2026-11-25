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
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    return re.sub(r"--[^\n]*", " ", sql)


def split_sql(sql):
    statements, current = [], ""
    for ch in sql:
        current += ch
        if ch == ";" and sqlite3.complete_statement(current):
            statements.append(current)
            current = ""
    statements.append(current)
    return [s.strip() for s in statements if strip_comments(s).strip()]


EXTRA_SQL = """INSERT INTO users (id, name, email, password_hash, phone) VALUES
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
            self.fail(f"{name} has no SQL in it yet. Write your SQL below the comments.")
        return sql, statements

    def run_sql(self, conn, statements, where=""):
        results = []
        for statement in statements:
            try:
                cursor = conn.execute(statement)
            except sqlite3.Error as error:
                self.fail(f"{where}Your SQL gave an error: {error}\nThe statement was:\n{statement}")
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
            self.fail(f"{where}Your query returns {len(got_cols)} column(s), but it should return "
                      f"{len(exp_cols)}. Check the list of columns after SELECT.")
        if names:
            for g, e in zip(got_cols, exp_cols):
                if g.lower() != e.lower():
                    self.fail(f"{where}A column should be called {e}, but yours is called {g}. "
                              f"Use AS to name it.")
        got = [tuple(norm(v) for v in r) for r in got]
        exp = [tuple(norm(v) for v in r) for r in exp]
        if len(got) != len(exp):
            self.fail(f"{where}Your query returned {len(got)} row(s), but it should return {len(exp)}.")
        remaining = list(got)
        missing = []
        for row in exp:
            if row in remaining:
                remaining.remove(row)
            else:
                missing.append(row)
        if missing:
            self.fail(f"{where}The rows are not right.\nThis row is missing: {show_row(missing[0])}\n"
                      f"This row should not be there: {show_row(remaining[0])}")
        if ordered and got != exp:
            self.fail(f"{where}The rows are right, but they are in the wrong order. Check your ORDER BY.")

    def check_keywords(self, sql):
        clean = strip_comments(sql)
        for word in self.MUST_USE:
            if not re.search(r"\b" + re.escape(word).replace("\\ ", "\\s+") + r"\b", clean, re.I):
                self.fail(f"Your SQL should use {word} for this task.")
        for word in self.MUST_NOT_USE:
            if re.search(r"\b" + re.escape(word).replace("\\ ", "\\s+") + r"\b", clean, re.I):
                self.fail(f"Do not use {word} in this task.")

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
            self.fail(f"{message} SQLite said: {error}")


def columns_of(conn, table):
    """Map column name to (type, notnull, default, pk position)."""
    return {row[1].lower(): (row[2].upper(), row[3], row[4], row[5])
            for row in conn.execute(f"PRAGMA table_info({table})")}


def foreign_keys_of(conn, table):
    """List of (from column, to table, to column, on delete)."""
    return [(row[3].lower(), row[2].lower(), (row[4] or "").lower(), row[6].upper())
            for row in conn.execute(f"PRAGMA foreign_key_list({table})")]


def table_exists(conn, table):
    return conn.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ? COLLATE NOCASE",
                        (table,)).fetchone() is not None


import tempfile


def connect():
    """A fresh Lakeview database in a temporary file, as the app would use it."""
    folder = tempfile.mkdtemp()
    path = Path(folder) / "test.db"
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(read("lakeview.sql"))
    conn.commit()
    return conn, path


def load():
    if "hotel_db" in sys.modules:
        return importlib.reload(sys.modules["hotel_db"])
    return importlib.import_module("hotel_db")


def check_placeholders(test, func):
    source = inspect.getsource(func)
    test.assertIn("?", source, f"{func.__name__} should use ? placeholders for the values.")
    for bad, why in [('f"', "an f-string"), ("f'", "an f-string"), (".format(", "format()"), ("%", "%")]:
        test.assertNotIn(bad, source, f"{func.__name__} builds SQL with {why}. Use ? placeholders instead.")


class TestTask(unittest.TestCase):
    longMessage = False

    def setUp(self):
        self.db = load()
        self.conn, self.path = connect()

    def tearDown(self):
        self.conn.close()

    def test_1_found(self):
        row = self.db.find_room(self.conn, 312)
        self.assertIsNotNone(row, "find_room(conn, 312) returned None, but room 312 exists.")
        self.assertEqual((312, "Suite", 250.0), tuple(row), "find_room(conn, 312) returned the wrong row.")

    def test_2_missing(self):
        self.assertIsNone(self.db.find_room(self.conn, 999), "find_room(conn, 999) should return None.")

    def test_3_placeholders(self):
        check_placeholders(self, self.db.find_room)
        self.assertIsNone(self.db.find_room(self.conn, "0 OR 1=1"),
                          "find_room returned a room for the input 0 OR 1=1. Use a ? placeholder.")
