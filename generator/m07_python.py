# SPDX-FileCopyrightText: 2026 Ross (pfate.xyz)
# SPDX-License-Identifier: GPL-3.0-or-later
from textwrap import dedent

from lib import Lesson, Module, P, Task, fixed
from shared import LAKEVIEW_SQL, choice, py_task

HEADER = '''\
"""Lakeview database functions.

Every function takes an open sqlite3 connection as its first argument.
The tests pass in a connection to a fresh copy of the Lakeview database
with row_factory set to sqlite3.Row.
"""

import sqlite3
'''

DEMO = '''

if __name__ == "__main__":
    # Try your functions here. Right-click this file and choose Run.
    from pathlib import Path

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((Path(__file__).parent / "lakeview.sql").read_text(encoding="utf-8"))
{demo}
'''

# Each function: (name, signature, docstring, solution body, placeholder, demo line)
FUNCTIONS = [
    ("get_rooms", "def get_rooms(conn):",
     "Return the number, room_type, and price_per_night of every room, sorted by number.",
     '''return conn.execute(
        "SELECT number, room_type, price_per_night FROM rooms ORDER BY number"
    ).fetchall()''',
     "pass  # Run the query and return fetchall()",
     "    for room in get_rooms(conn):\n        print(tuple(room))"),
    ("find_room", "def find_room(conn, number):",
     "Return the number, room_type, and price_per_night of the room with this number, or None.",
     '''return conn.execute(
        "SELECT number, room_type, price_per_night FROM rooms WHERE number = ?",
        (number,),
    ).fetchone()''',
     "pass  # Use a ? placeholder for number, then return fetchone()",
     "    print(find_room(conn, 312) and tuple(find_room(conn, 312)))\n    print(find_room(conn, 999))"),
    ("add_extra", "def add_extra(conn, name, price):",
     "Add an extra, save the change, and return the new extra's id.",
     '''cursor = conn.execute("INSERT INTO extras (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    return cursor.lastrowid''',
     "pass  # INSERT with two ? placeholders, commit, then return cursor.lastrowid",
     "    print(add_extra(conn, 'Dinner', 30.0))"),
    ("register", "def register(conn, name, email):",
     "Add a user with password_hash 'demo-hash' and return a message for the user.",
     '''try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, 'demo-hash')",
            (name, email),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return "That email address is already registered."
    return "Account created."''',
     "pass  # Try the INSERT and commit. Catch sqlite3.IntegrityError.",
     "    print(register(conn, 'Maria', 'maria@example.com'))\n    print(register(conn, 'Maria', 'maria@example.com'))"),
    ("bookings_for", "def bookings_for(conn, email):",
     "Return a list of dicts with number, check_in, and check_out for this guest's bookings, sorted by check_in.",
     '''rows = conn.execute(
        """
        SELECT r.number, b.check_in, b.check_out
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN rooms r ON b.room_id = r.id
        WHERE u.email = ?
        ORDER BY b.check_in
        """,
        (email,),
    ).fetchall()
    return [dict(row) for row in rows]''',
     "pass  # JOIN bookings, users, and rooms, filter by email with ?, return a list of dicts",
     "    print(bookings_for(conn, 'james@example.com'))"),
]


def module_parts(upto):
    """hotel_db.py with functions 0..upto-1 solved and function upto as the task."""
    parts = [HEADER]
    demos = []
    for i, (name, sig, doc, body, ph, demo) in enumerate(FUNCTIONS[:upto + 1]):
        parts.append(f'\n\n{sig}\n    """{doc}"""\n    ')
        parts.append(P(body, ph) if i == upto else body)
        parts.append("\n")
        demos.append(demo)
    parts.append(DEMO.format(demo="\n".join(demos)))
    return parts


TEST_HEAD = '''
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
'''

TESTS = [
    '''
    def test_1_rooms(self):
        result = self.db.get_rooms(self.conn)
        self.assertIsNotNone(result, "get_rooms should return the rows, not None.")
        rows = [tuple(r) for r in result]
        self.assertEqual(5, len(rows), f"get_rooms should return 5 rooms, but it returned {len(rows)}.")
        self.assertEqual((101, "Single", 80.0), rows[0], "The first room should be (101, 'Single', 80.0).")
        self.assertEqual((312, "Suite", 250.0), rows[-1], "The last room should be (312, 'Suite', 250.0).")
''',
    '''
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
''',
    '''
    def test_1_returns_id(self):
        new_id = self.db.add_extra(self.conn, "Dinner", 30.0)
        self.assertEqual(5, new_id, "add_extra should return the new id, which is 5 here. Use cursor.lastrowid.")

    def test_2_saved(self):
        self.db.add_extra(self.conn, "Dinner", 30.0)
        other = sqlite3.connect(self.path)
        row = other.execute("SELECT name, price FROM extras WHERE name = 'Dinner'").fetchone()
        other.close()
        self.assertEqual(("Dinner", 30.0), row,
                         "The new extra was not saved. Did you call conn.commit()?")

    def test_3_placeholders(self):
        check_placeholders(self, self.db.add_extra)
''',
    '''
    def test_1_created(self):
        self.assertEqual("Account created.", self.db.register(self.conn, "Maria", "maria@example.com"),
                         "A new email should give the message Account created.")
        other = sqlite3.connect(self.path)
        row = other.execute("SELECT name FROM users WHERE email = 'maria@example.com'").fetchone()
        other.close()
        self.assertIsNotNone(row, "Maria was not saved. Did you call conn.commit()?")

    def test_2_duplicate(self):
        try:
            message = self.db.register(self.conn, "James", "james@example.com")
        except sqlite3.IntegrityError:
            self.fail("register let an IntegrityError escape. Catch it with try and except.")
        self.assertEqual("That email address is already registered.", message,
                         "An email that is already used should give the message That email address is already registered.")

    def test_3_placeholders(self):
        check_placeholders(self, self.db.register)
''',
    '''
    def test_1_james(self):
        result = self.db.bookings_for(self.conn, "james@example.com")
        self.assertIsInstance(result, list, "bookings_for should return a list.")
        self.assertEqual([
            {"number": 101, "check_in": "2026-11-01", "check_out": "2026-11-04"},
            {"number": 101, "check_in": "2026-12-01", "check_out": "2026-12-03"},
        ], result, "bookings_for returned the wrong list for james@example.com.")

    def test_2_nobody(self):
        self.assertEqual([], self.db.bookings_for(self.conn, "eileen@example.com"),
                         "A guest with no bookings should give an empty list.")

    def test_3_placeholders(self):
        check_placeholders(self, self.db.bookings_for)
''',
]

PY_THEORY = Task(
    "t01-sqlite3", "SQL from Python", "theory",
    dedent("""
    Your Flask app talks to SQLite through Python's `sqlite3` module. The SQL is the same as in the earlier modules. What is new is how you send it and get the results back.

    ```python
    import sqlite3

    conn = sqlite3.connect("hotel.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    rows = conn.execute("SELECT number, price_per_night FROM rooms").fetchall()
    for row in rows:
        print(row["number"], row["price_per_night"])
    ```

    | Code | What it does |
    |---|---|
    | `conn.execute(sql, values)` | runs one statement and returns a cursor |
    | `.fetchall()` | every row, as a list |
    | `.fetchone()` | the first row, or `None` if there are none |
    | `cursor.lastrowid` | the id given to the row you just inserted |
    | `conn.commit()` | saves your changes |
    | `conn.row_factory = sqlite3.Row` | lets you read columns by name, like `row["number"]` |
    | `dict(row)` | turns a `sqlite3.Row` into a dictionary |

    ## Placeholders

    Never put a value into SQL by joining strings or with an f-string. Use a `?` in the SQL for each value and pass the values as a tuple:

    ```python
    conn.execute("SELECT * FROM users WHERE email = ?", (email,))
    ```

    The comma in `(email,)` matters. Without it, Python sees a string in brackets, not a tuple.

    Placeholders stop SQL injection, where a user types SQL into a form and your app runs it. They also deal with quotes in names such as O'Brien.

    ## commit

    `sqlite3` starts a transaction before any `INSERT`, `UPDATE`, or `DELETE`. Nothing is saved until you call `conn.commit()`. Forgetting it is a common reason for "my form says it worked but nothing is in the database".

    ## Errors

    When a constraint is broken, `sqlite3` raises `sqlite3.IntegrityError`. Catch it and give the user a helpful message instead of a crash:

    ```python
    try:
        conn.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", (name, email, pw))
        conn.commit()
    except sqlite3.IntegrityError:
        return "That email address is already registered."
    ```

    In these tasks you write functions in `hotel_db.py`. Each one takes the connection as its first argument, so the tests can hand it a fresh database. Run `example.py` to see the code above working.
    """).strip() + "\n",
    [fixed("example.py", dedent('''\
        import sqlite3
        from pathlib import Path

        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript((Path(__file__).parent / "lakeview.sql").read_text(encoding="utf-8"))

        for row in conn.execute("SELECT number, price_per_night FROM rooms").fetchall():
            print(row["number"], row["price_per_night"])

        email = "mary@example.com"
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        print(dict(user))

        try:
            conn.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                         ("Mary again", email, "demo-hash"))
        except sqlite3.IntegrityError as error:
            print("Refused:", error)
        ''')),
     fixed("lakeview.sql", LAKEVIEW_SQL, editable=False)],
)

TASK_TEXT = [
    (['rooms'], "t02-get-rooms", "Fetching rows", """
     Complete `get_rooms` in `hotel_db.py`. It should run a query and return the `number`, `room_type`, and `price_per_night` of every room, sorted by `number`.

     Use `conn.execute(...)` and return the result of `.fetchall()`. Run `hotel_db.py` to see what your function returns.
     """),
    (['rooms'], "t03-find-room", "Using a placeholder", """
     Complete `find_room`. It should return the `number`, `room_type`, and `price_per_night` of the room with the given `number`, or `None` if there is no such room.

     Use a `?` placeholder for the number and pass `(number,)` as the second argument to `execute`. Then use `.fetchone()`, which gives `None` when no row matches.
     """),
    (['extras'], "t04-add-extra", "Inserting and committing", """
     Complete `add_extra`. It should:

     1. insert a row into `extras` with the given `name` and `price`, using `?` placeholders
     2. call `conn.commit()`
     3. return the new row's id, from `cursor.lastrowid`

     The tests check that the row is saved by opening a second connection to the same database file. Without `commit()`, the second connection cannot see it.
     """),
    (['users'], "t05-register", "Catching IntegrityError", """
     Complete `register`. It inserts a user with the given `name` and `email` and the `password_hash` `demo-hash`, then commits.

     `email` is `UNIQUE`, so registering an email twice raises `sqlite3.IntegrityError`. Catch it and return a message instead. Return these messages exactly, including the full stop:

     - success: `Account created.`
     - email already used: `That email address is already registered.`
     """),
    (['bookings', 'users', 'rooms'], "t06-bookings-for", "Joins from Python", """
     Complete `bookings_for`. Given a guest's email, it returns a list of their bookings, sorted by `check_in`. Each booking is a dictionary with the keys `number` (the room number), `check_in` and `check_out`.

     You need to join `bookings`, `users`, and `rooms`. Because the connection uses `sqlite3.Row`, `dict(row)` turns each row into a dictionary with the column names as keys.

     A guest with no bookings gives an empty list.
     """),
]

PY_TASKS = [
    py_task(slug, title, text, "hotel_db.py", module_parts(i), TEST_HEAD + tests, tables=tables)
    for i, ((tables, slug, title, text), tests) in enumerate(zip(TASK_TEXT, TESTS))
]

QUIZ = choice(
    "t07-safe-query-quiz", "Quiz: which query is safe?",
    """
    `email` comes from a form that anyone can fill in. Which line is safe from SQL injection?
    """,
    ['conn.execute("SELECT * FROM users WHERE email = ?", (email,))',
     'conn.execute(f"SELECT * FROM users WHERE email = \'{email}\'")',
     'conn.execute("SELECT * FROM users WHERE email = \'" + email + "\'")',
     'conn.execute("SELECT * FROM users WHERE email = \'%s\'" % email)'],
    correct=[0],
    incorrect="Not quite. Three of these paste the user's text straight into the SQL. Only one passes it to SQLite separately.",
)

MODULE = Module("m07-sql-from-python", "SQL from Python", [
    Lesson("l01-sqlite3", "The sqlite3 module", [PY_THEORY] + PY_TASKS + [QUIZ]),
])
