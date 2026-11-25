# SPDX-FileCopyrightText: 2026 Ross (pfate.xyz)
# SPDX-License-Identifier: GPL-3.0-or-later
from lib import Lesson, Module, P
from shared import choice, select_task, theory

WELCOME = theory(
    "t01-welcome", "Welcome to the Lakeview Hotel",
    """
    This course is for practising SQL with SQLite. It uses a small database for the Lakeview Hotel, on the shore of Toluca Lake. The same database is used in every task, so you get to know the data well.

    ## How the tasks work

    Most tasks give you a file called `task.sql`. You write your SQL in that file and press Check. Hidden tests then run your SQL against a fresh copy of the database and compare what it does with what it should do. If something is wrong, the message tells you what to look at.

    Each task folder also has two locked files:

    - `lakeview.sql` builds the database. Open it to see every table and every row.
    - `run.py` runs your SQL and prints the results. Right-click it and choose Run, or open it and press the green arrow.

    Run your SQL before you press Check. Seeing the rows is the fastest way to spot a mistake.

    The tests run your SQL a second time with some extra rows added to the database. This stops an answer that types out the expected rows by hand from passing. Write SQL that would still work if the data changed.

    ## Browsing the database (optional)

    You do not need anything beyond `run.py` for this course. If you would like to click through the tables as well, every run of `run.py` saves a copy of the result as `practice.db` in the task folder. You can open it with:

    - the Database tool window in the paid version of PyCharm: press +, then Data Source, then SQLite, and choose `practice.db`
    - DB Browser for SQLite, a free program from sqlitebrowser.org

    If `run.py` says that `practice.db` is in use, close it in the other program and run again.

    ## The Lakeview tables

    | Table | What it holds |
    |---|---|
    | `users` | Guests who have an account |
    | `rooms` | The five hotel rooms, with type, capacity, and nightly price |
    | `bookings` | Who booked which room, the dates, the number of guests, and the total price |
    | `extras` | Things a guest can add to a stay, such as breakfast |
    | `booking_extras` | Which extras were added to which booking, and how many |

    The file `examples.sql` in this task has a first query in it. Run `run.py` now to see the output, then move on.
    """,
    examples="""
    -- Run run.py to see the result of this query.
    SELECT * FROM rooms;
    """,
)

FIRST_SELECT = select_task(
    "t02-first-select", "Your first SELECT",
    """
    `SELECT` reads rows from a table. The star means every column.

    ```sql
    SELECT * FROM users;
    ```

    In `task.sql`, replace the word `table_name` so that the query shows every column of every row in the `bookings` table.
    """,
    ["Show every column of every row in the bookings table."],
    solution=None, sql_parts=["SELECT * FROM ", P("bookings", "table_name"), ";"],
    tables=['bookings'],
)

COLUMNS = select_task(
    "t03-choosing-columns", "Choosing columns",
    """
    You rarely need every column. List the columns you want after `SELECT`, separated by commas.

    ```sql
    SELECT name, email FROM users;
    ```

    Write a query that shows the `number`, `room_type`, and `price_per_night` of every room in the `rooms` table.
    """,
    ["Show the number, room_type, and price_per_night of every room."],
    solution="SELECT number, room_type, price_per_night FROM rooms;",
    names=True,
    tables=['rooms'],
)

FILTER_THEORY = theory(
    "t01-filtering", "Filtering and sorting",
    """
    `WHERE` keeps only the rows that match a condition.

    ```sql
    SELECT number, price_per_night FROM rooms WHERE price_per_night > 100;
    ```

    ## Comparison operators

    | Operator | Meaning |
    |---|---|
    | `=` | equal to |
    | `<>` or `!=` | not equal to |
    | `<`, `<=`, `>`, `>=` | less than, at most, more than, at least |
    | `BETWEEN a AND b` | from a to b, including both ends |
    | `IN (a, b, c)` | equal to one of the values in the list |
    | `LIKE 'pattern'` | text matching a pattern, where `%` means any characters and `_` means one character |
    | `IS NULL`, `IS NOT NULL` | the value is missing, or is not missing |

    Text goes in single quotes: `'Double'`. Numbers do not: `120`.

    Combine conditions with `AND` and `OR`. Use brackets when you mix them, so that SQLite does what you mean.

    ```sql
    SELECT number FROM rooms WHERE available = 1 AND (room_type = 'Double' OR room_type = 'Suite');
    ```

    ## Sorting and limiting

    `ORDER BY` sorts the rows. Add `DESC` for largest first. You can sort by more than one column: the second column only matters when the first is tied.

    ```sql
    SELECT number, room_type, price_per_night FROM rooms ORDER BY room_type, price_per_night DESC;
    ```

    `LIMIT n` keeps only the first n rows. It goes at the very end. `DISTINCT` removes repeated rows.

    ```sql
    SELECT DISTINCT room_type FROM rooms;
    ```

    ## NULL

    `NULL` means "no value". In Lakeview, some guests have not given a phone number, so their `phone` is `NULL`. Nothing is ever equal to `NULL`, not even `NULL` itself, so `phone = NULL` never matches anything. Use `phone IS NULL` instead.

    Try the queries in `examples.sql` with `run.py`, and change them to see what happens.
    """,
    examples="""
    SELECT number, price_per_night FROM rooms WHERE price_per_night > 100;

    SELECT number FROM rooms WHERE available = 1 AND (room_type = 'Double' OR room_type = 'Suite');

    SELECT number, room_type, price_per_night FROM rooms ORDER BY room_type, price_per_night DESC;

    SELECT DISTINCT room_type FROM rooms;

    SELECT name, phone FROM users WHERE phone IS NULL;
    """,
)

WHERE = select_task(
    "t02-where", "Rooms under 150 a night",
    """
    Write a query that shows the `number` and `price_per_night` of every room that costs less than 150 a night.
    """,
    ["Show the number and price_per_night of rooms that cost less than 150 a night."],
    solution="SELECT number, price_per_night FROM rooms WHERE price_per_night < 150;",
    must_use=["WHERE"],
    tables=['rooms'],
)

AND_OR = select_task(
    "t03-and-or", "Available rooms for two",
    """
    The `available` column is `1` when a room can be booked and `0` when it cannot.

    Write a query that shows the `number` and `room_type` of rooms that are available and hold at least 2 guests (`capacity`).
    """,
    ["Show the number and room_type of rooms that are available",
     "and have a capacity of at least 2."],
    solution="SELECT number, room_type FROM rooms WHERE available = 1 AND capacity >= 2;",
    must_use=["AND"],
    tables=['rooms'],
)

ORDER = select_task(
    "t04-order-by", "Most expensive first",
    """
    Write a query that shows the `number`, `room_type`, and `price_per_night` of every room, with the most expensive room first.
    """,
    ["Show number, room_type, and price_per_night of every room,",
     "most expensive first."],
    solution="SELECT number, room_type, price_per_night FROM rooms ORDER BY price_per_night DESC;",
    ordered=True, must_use=["ORDER BY"],
    tables=['rooms'],
)

LIKE = select_task(
    "t05-like", "Finding names with LIKE",
    """
    `LIKE` matches text against a pattern. `%` stands for any number of characters, including none.

    ```sql
    SELECT name FROM users WHERE name LIKE 'J%';
    ```

    Write a query that shows the `name` and `email` of every guest whose surname is Mason. The surname is the last word in `name`.
    """,
    ["Show the name and email of every guest whose surname is Mason."],
    solution="SELECT name, email FROM users WHERE name LIKE '% Mason';",
    must_use=["LIKE"],
    tables=['users'],
)

BETWEEN = select_task(
    "t06-between-dates", "Bookings in November",
    """
    Dates in Lakeview are stored as text in the form `YYYY-MM-DD`, for example `2026-11-04`. Text in this form sorts in date order, so `<`, `>`, and `BETWEEN` work on it.

    Write a query that shows the `id`, `check_in`, and `check_out` of every booking with a `check_in` date in November 2026.
    """,
    ["Show id, check_in, and check_out of bookings that check in during November 2026."],
    solution="SELECT id, check_in, check_out FROM bookings WHERE check_in BETWEEN '2026-11-01' AND '2026-11-30';",
    tables=['bookings'],
)

LIMIT = select_task(
    "t07-limit", "The three cheapest rooms",
    """
    Write a query that shows the `number` and `price_per_night` of the three cheapest rooms, cheapest first.
    """,
    ["Show the number and price_per_night of the three cheapest rooms, cheapest first."],
    solution="SELECT number, price_per_night FROM rooms ORDER BY price_per_night LIMIT 3;",
    ordered=True, must_use=["ORDER BY", "LIMIT"],
    tables=['rooms'],
)

NULLS = select_task(
    "t08-is-null", "Guests with no phone number",
    """
    Write a query that shows the `name` and `email` of every guest who has not given a phone number.

    Remember that `= NULL` never matches anything.
    """,
    ["Show the name and email of guests with no phone number."],
    solution="SELECT name, email FROM users WHERE phone IS NULL;",
    must_use=["IS NULL"],
    tables=['users'],
)

FIX = select_task(
    "t09-fix-the-query", "Fix the query",
    """
    A colleague wrote a query to list the `number` and `room_type` of every room that can be booked. It runs without an error, but the output is wrong.

    Run it with `run.py` and look closely at the column headings and the number of rows. Then fix it. There are two mistakes.
    """,
    ["This query should show the number and room_type of every room that can be booked.",
     "It has two mistakes. Fix them."],
    solution="SELECT number, room_type FROM rooms WHERE available = 1;",
    placeholder="SELECT number room_type FROM rooms WHERE available = 'yes';",
    names=True,
    tables=['rooms'],
)

NULL_QUIZ = choice(
    "t10-null-quiz", "Quiz: NULL",
    """
    Harry Mason has no phone number. Which query finds him?
    """,
    ["SELECT name FROM users WHERE phone IS NULL;",
     "SELECT name FROM users WHERE phone = NULL;",
     "SELECT name FROM users WHERE phone = '';",
     "SELECT name FROM users WHERE phone = 0;"],
    correct=[0],
    incorrect="Not quite. NULL means no value at all, so it is never equal to anything. Which operator checks for a missing value?",
)

MODULE = Module("m01-reading-data", "Reading Data", [
    Lesson("l01-getting-started", "Getting started", [WELCOME, FIRST_SELECT, COLUMNS]),
    Lesson("l02-filtering-and-sorting", "Filtering and sorting",
           [FILTER_THEORY, WHERE, AND_OR, ORDER, LIKE, BETWEEN, LIMIT, NULLS, FIX, NULL_QUIZ]),
])
