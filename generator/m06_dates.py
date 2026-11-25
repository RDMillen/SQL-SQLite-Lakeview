# SPDX-FileCopyrightText: 2026 Ross (pfate.xyz)
# SPDX-License-Identifier: GPL-3.0-or-later
from lib import Lesson, Module
from shared import choice, select_task, theory

DATES_THEORY = theory(
    "t01-dates", "Working with dates",
    """
    Lakeview stores dates as text in the form `YYYY-MM-DD`. SQLite has functions that understand this form.

    | Expression | Result |
    |---|---|
    | `date('2026-11-01', '+3 days')` | `2026-11-04` |
    | `date('2026-11-30', '+1 month')` | `2026-12-30` |
    | `date('now')` | today's date |
    | `julianday('2026-11-04') - julianday('2026-11-01')` | `3.0` |

    `julianday` turns a date into a number of days, so subtracting two of them gives the number of nights between check-in and check-out. The result is a `REAL`. Wrap it in `CAST(... AS INTEGER)` to get a whole number.

    ```sql
    SELECT id, CAST(julianday(check_out) - julianday(check_in) AS INTEGER) AS nights
    FROM bookings;
    ```

    Because the dates are in `YYYY-MM-DD` form, comparing them as text also compares them as dates: `'2026-11-04' < '2026-12-01'` is true. This only works if every date is stored the same way, with leading zeros.

    ## When do two stays clash?

    A room cannot be booked by two people on the same night. A new stay from `new_in` to `new_out` clashes with an existing stay when both of these are true:

    ```text
    new_in < existing_out
    new_out > existing_in
    ```

    The check-out day is not a night in the room, so back-to-back stays are fine. James checks out of room 101 on 4 November and Heather checks in on 4 November, and there is no clash.

    Here is the night-by-night picture for room 101 in early November. Each column is a night, starting on that date.

    ```text
    Night of          1   2   3   4   5   6
    James  1 to 4     X   X   X
    Heather 4 to 7                X   X   X
    New    3 to 5             ?   ?
    ```

    The new stay wants the nights of the 3rd and the 4th. James has the 3rd and Heather has the 4th, so it clashes with both.
    """,
    examples="""
    SELECT date('2026-11-01', '+3 days') AS three_days_later;

    SELECT id, check_in, check_out,
           CAST(julianday(check_out) - julianday(check_in) AS INTEGER) AS nights
    FROM bookings;
    """,
)

NIGHTS = select_task(
    "t02-nights", "Nights per booking",
    """
    Write a query that shows each booking's `id` and the number of nights as a whole number, in a column called `nights`. Sort by `id`.
    """,
    ["Show each booking's id and its number of nights as a whole number.",
     "Name the column nights. Sort by id."],
    solution="""
    SELECT id, CAST(julianday(check_out) - julianday(check_in) AS INTEGER) AS nights
    FROM bookings
    ORDER BY id;
    """,
    names=True, ordered=True, must_use=["julianday"],
    tables=['bookings'],
)

LONG = select_task(
    "t03-long-stays", "Long stays",
    """
    Write a query that shows the `id`, `check_in`, and `check_out` of every booking that lasts more than 2 nights.
    """,
    ["Show id, check_in, and check_out of bookings longer than 2 nights."],
    solution="""
    SELECT id, check_in, check_out
    FROM bookings
    WHERE julianday(check_out) - julianday(check_in) > 2;
    """,
    tables=['bookings'],
)

OVERLAP = select_task(
    "t04-find-the-clashes", "Find the clashes",
    """
    A guest asks for room 101 from `2026-11-03` to `2026-11-05`. Write a query that shows the `id`, `check_in`, and `check_out` of every existing booking of room 101 that clashes with this stay.

    Use the clash rule from the start of this lesson. Room 101 has `id` 1 in the `rooms` table.
    """,
    ["Show id, check_in, and check_out of bookings for room 101 that clash with",
     "a new stay from 2026-11-03 to 2026-11-05."],
    solution="""
    SELECT id, check_in, check_out
    FROM bookings
    WHERE room_id = 1
      AND check_in < '2026-11-05'
      AND check_out > '2026-11-03';
    """,
    tables=['bookings', 'rooms'],
)

SUB_THEORY = theory(
    "t01-subqueries", "Subqueries",
    """
    A subquery is a query inside another query, in brackets. SQLite runs it and uses its result.

    ## A single value

    This finds the rooms that cost more than the average room:

    ```sql
    SELECT number, price_per_night
    FROM rooms
    WHERE price_per_night > (SELECT AVG(price_per_night) FROM rooms);
    ```

    ## A list with IN

    A subquery can give a list of values for `IN`. This finds the guests who have booked room id 5:

    ```sql
    SELECT name FROM users
    WHERE id IN (SELECT user_id FROM bookings WHERE room_id = 5);
    ```

    ## EXISTS and NOT EXISTS

    `EXISTS (subquery)` is true when the subquery finds at least one row. `NOT EXISTS` is true when it finds none. The subquery can use columns from the outer query, so it is worked out again for each outer row.

    This finds the rooms with no bookings in December:

    ```sql
    SELECT r.number
    FROM rooms r
    WHERE NOT EXISTS (
        SELECT 1 FROM bookings b
        WHERE b.room_id = r.id
          AND b.check_in BETWEEN '2026-12-01' AND '2026-12-31'
    );
    ```

    `SELECT 1` is a habit: `EXISTS` only cares whether a row was found, not what is in it.

    Put `NOT EXISTS` together with the clash rule and you have the query behind a "rooms free on these dates" search.
    """,
    examples="""
    SELECT number, price_per_night
    FROM rooms
    WHERE price_per_night > (SELECT AVG(price_per_night) FROM rooms);

    SELECT r.number
    FROM rooms r
    WHERE NOT EXISTS (
        SELECT 1 FROM bookings b
        WHERE b.room_id = r.id
          AND b.check_in BETWEEN '2026-12-01' AND '2026-12-31'
    );
    """,
)

ABOVE_AVG = select_task(
    "t02-above-average", "Cheaper than average",
    """
    Write a query that shows the `number` and `price_per_night` of every room that costs less than the average room. Use a subquery for the average.
    """,
    ["Show number and price_per_night of rooms cheaper than the average room.",
     "Use a subquery."],
    solution="""
    SELECT number, price_per_night
    FROM rooms
    WHERE price_per_night < (SELECT AVG(price_per_night) FROM rooms);
    """,
    must_use=["AVG"],
    tables=['rooms'],
)

IN_SUB = select_task(
    "t03-in-subquery", "Who has stayed in the Suite?",
    """
    Write a query that shows the `name` of every guest who has a booking for the Suite, room number 312. Each guest should appear once. Sort by `name`.

    You can use subqueries with `IN`, or a join with `DISTINCT`. Do not type the room's `id`: find it from the room number.
    """,
    ["Show the name of every guest with a booking for room number 312.",
     "Each guest once. Sort by name."],
    solution="""
    SELECT name FROM users
    WHERE id IN (
        SELECT user_id FROM bookings
        WHERE room_id = (SELECT id FROM rooms WHERE number = 312)
    )
    ORDER BY name;
    """,
    ordered=True,
    tables=['users', 'bookings', 'rooms'],
)

FREE = select_task(
    "t04-free-rooms", "Rooms free on these dates",
    """
    A guest wants a room from `2026-12-01` to `2026-12-03`. Write a query that shows the `number` of every room that:

    - is available (`available = 1`)
    - has no booking that clashes with those dates

    Use `NOT EXISTS` with the clash rule. Sort by `number`.
    """,
    ["Show the number of every available room with no clashing booking",
     "for a stay from 2026-12-01 to 2026-12-03. Sort by number."],
    solution="""
    SELECT r.number
    FROM rooms r
    WHERE r.available = 1
      AND NOT EXISTS (
          SELECT 1 FROM bookings b
          WHERE b.room_id = r.id
            AND b.check_in < '2026-12-03'
            AND b.check_out > '2026-12-01'
      )
    ORDER BY r.number;
    """,
    ordered=True, must_use=["NOT EXISTS"],
    tables=['rooms', 'bookings'],
)

QUIZ = choice(
    "t05-back-to-back-quiz", "Quiz: back-to-back stays",
    """
    Room 201 is booked from `2026-12-20` to `2026-12-27`. Which new stays in room 201 clash with it? Choose every one that clashes.
    """,
    ["2026-12-18 to 2026-12-21", "2026-12-27 to 2026-12-29",
     "2026-12-15 to 2026-12-20", "2026-12-22 to 2026-12-23"],
    correct=[0, 3], multiple=True,
    incorrect="Not quite. A stay clashes when new_in < existing_out and new_out > existing_in. Arriving on the day someone leaves is fine.",
)

MODULE = Module("m06-dates-and-subqueries", "Dates and Subqueries", [
    Lesson("l01-dates", "Dates and clashes", [DATES_THEORY, NIGHTS, LONG, OVERLAP]),
    Lesson("l02-subqueries", "Subqueries", [SUB_THEORY, ABOVE_AVG, IN_SUB, FREE, QUIZ]),
])
