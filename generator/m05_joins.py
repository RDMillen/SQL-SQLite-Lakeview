from lib import Lesson, Module
from shared import choice, select_task, theory

JOIN_THEORY = theory(
    "t01-joins", "Joining tables",
    """
    A booking row only holds `user_id` and `room_id`. To show the guest's name and the room number, you join `bookings` to `users` and `rooms`.

    ```sql
    SELECT bookings.id, users.name, rooms.number
    FROM bookings
    JOIN users ON bookings.user_id = users.id
    JOIN rooms ON bookings.room_id = rooms.id;
    ```

    `ON` says how the rows match: the foreign key on one side equals the primary key on the other. `JOIN` on its own means `INNER JOIN`. It keeps only the rows that have a match on both sides.

    ## Table names and aliases

    When two tables have a column with the same name, such as `id`, you must say which one you mean: `bookings.id` or `users.id`. If you do not, SQLite gives the error `ambiguous column name: id`.

    Typing full table names gets long. An alias is a short name for a table, given straight after it:

    ```sql
    SELECT b.id, u.name, r.number
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN rooms r ON b.room_id = r.id;
    ```

    ## LEFT JOIN

    `LEFT JOIN` keeps every row from the table on the left, even when there is no match on the right. The columns from the right-hand table are `NULL` for those rows. This is how you find things that have never happened, such as rooms that have never been booked:

    ```sql
    SELECT r.number, b.id
    FROM rooms r
    LEFT JOIN bookings b ON b.room_id = r.id
    WHERE b.id IS NULL;
    ```

    ## Joining more tables

    Each extra table needs its own `JOIN ... ON`. To get from a guest to the extras on their bookings you follow the keys: `users` to `bookings`, `bookings` to `booking_extras`, `booking_extras` to `extras`. Look at `lakeview.sql` and trace the path before you write the query.

    ## Joins with GROUP BY

    You can group joined rows like any others. `COUNT(b.id)` counts only the rows where a booking was found, so with a `LEFT JOIN` it gives 0 for a guest with no bookings, where `COUNT(*)` would give 1.
    """,
    examples="""
    SELECT b.id, u.name, r.number
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN rooms r ON b.room_id = r.id;

    SELECT r.number, b.id
    FROM rooms r
    LEFT JOIN bookings b ON b.room_id = r.id;
    """,
)

TWO = select_task(
    "t02-two-tables", "Bookings with guest names",
    """
    Write a query that shows every booking's `id`, the guest's `name`, and the `check_in` date. Sort by the booking `id`.
    """,
    ["Show each booking's id, the guest's name, and check_in. Sort by booking id."],
    solution="""
    SELECT b.id, u.name, b.check_in
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    ORDER BY b.id;
    """,
    ordered=True, must_use=["JOIN"],
    tables=['bookings', 'users'],
)

FILTERED = select_task(
    "t03-join-and-where", "December bookings by room",
    """
    Write a query that shows the booking `id`, the room `number`, and the `room_type` for every booking that checks in during December 2026. Sort by the booking `id`.
    """,
    ["Show booking id, room number, and room_type for bookings checking in during December 2026.",
     "Sort by booking id."],
    solution="""
    SELECT b.id, r.number, r.room_type
    FROM bookings b
    JOIN rooms r ON b.room_id = r.id
    WHERE b.check_in BETWEEN '2026-12-01' AND '2026-12-31'
    ORDER BY b.id;
    """,
    ordered=True, must_use=["JOIN"],
    tables=['bookings', 'rooms'],
)

THREE = select_task(
    "t04-three-tables", "The booking list",
    """
    The front desk wants a booking list. Write a query that shows the guest's `name`, the room `number`, `check_in`, `check_out`, and `total_price` for every booking. Sort by `check_in`, then by room `number`.
    """,
    ["Show name, room number, check_in, check_out, and total_price for every booking.",
     "Sort by check_in, then room number."],
    solution="""
    SELECT u.name, r.number, b.check_in, b.check_out, b.total_price
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN rooms r ON b.room_id = r.id
    ORDER BY b.check_in, r.number;
    """,
    ordered=True, must_use=["JOIN"],
    tables=['bookings', 'users', 'rooms'],
)

NEVER = select_task(
    "t05-never-booked", "Rooms never booked",
    """
    Write a query that shows the `number` of every room that has no bookings at all. Use a `LEFT JOIN`.
    """,
    ["Show the number of every room that has never been booked. Use a LEFT JOIN."],
    solution="""
    SELECT r.number
    FROM rooms r
    LEFT JOIN bookings b ON b.room_id = r.id
    WHERE b.id IS NULL;
    """,
    must_use=["LEFT JOIN"],
    tables=['rooms', 'bookings'],
)

COUNT_ZERO = select_task(
    "t06-including-zero", "Every guest, even with no bookings",
    """
    Write a query that shows every guest's `name` and how many bookings they have, in a column called `bookings`. Guests with no bookings must appear with 0. Sort by `name`.

    Think about which table goes on the left of the `LEFT JOIN`, and what you count.
    """,
    ["Show every guest's name and number of bookings, including guests with 0.",
     "Name the count bookings. Sort by name."],
    solution="""
    SELECT u.name, COUNT(b.id) AS bookings
    FROM users u
    LEFT JOIN bookings b ON b.user_id = u.id
    GROUP BY u.id
    ORDER BY u.name;
    """,
    names=True, ordered=True, must_use=["LEFT JOIN", "GROUP BY"],
    tables=['users', 'bookings'],
)

FOUR = select_task(
    "t07-four-tables", "Extras for each guest",
    """
    Write a query that shows, for every extra added to a booking:

    - the guest's `name`
    - the booking's `check_in`
    - the extra's `name`
    - the `quantity`

    You need four tables. Two of them have a column called `name`, so give the extra's name the alias `extra`. Sort by the guest's name, then `check_in`, then `extra`.
    """,
    ["Show guest name, check_in, extra (the extra's name), and quantity for every extra on a booking.",
     "Sort by guest name, then check_in, then extra."],
    solution="""
    SELECT u.name, b.check_in, e.name AS extra, be.quantity
    FROM users u
    JOIN bookings b ON b.user_id = u.id
    JOIN booking_extras be ON be.booking_id = b.id
    JOIN extras e ON be.extra_id = e.id
    ORDER BY u.name, b.check_in, extra;
    """,
    names=True, ordered=True, must_use=["JOIN"],
    tables=['users', 'bookings', 'booking_extras', 'extras'],
)

TAKINGS = select_task(
    "t08-join-and-group", "Takings by room type",
    """
    Write a query that shows each `room_type` with the total `total_price` of its bookings, in a column called `takings`. Highest takings first. Room types with no bookings do not need to appear.
    """,
    ["Show each room_type and the total of total_price for its bookings.",
     "Name the total takings. Highest first."],
    solution="""
    SELECT r.room_type, SUM(b.total_price) AS takings
    FROM bookings b
    JOIN rooms r ON b.room_id = r.id
    GROUP BY r.room_type
    ORDER BY takings DESC;
    """,
    names=True, ordered=True, must_use=["JOIN", "GROUP BY"],
    tables=['bookings', 'rooms'],
)

FIX = select_task(
    "t09-fix-the-join", "Fix the join",
    """
    This query should show each booking's `id`, the guest's `name`, and the room `number`, sorted by booking `id`. Run it and read the error. Then fix it.
    """,
    ["This should show each booking's id, the guest's name, and the room number.",
     "Run it, read the error, then fix it."],
    solution="""
    SELECT bookings.id, name, number
    FROM bookings
    JOIN users ON user_id = users.id
    JOIN rooms ON room_id = rooms.id
    ORDER BY bookings.id;
    """,
    placeholder="""
    SELECT id, name, number
    FROM bookings
    JOIN users ON user_id = users.id
    JOIN rooms ON room_id = rooms.id
    ORDER BY id;
    """,
    ordered=True,
    tables=['bookings', 'users', 'rooms'],
)

QUIZ = choice(
    "t10-inner-or-left", "Quiz: INNER or LEFT",
    """
    There are 6 guests. Eileen Galvin has no bookings. How many rows does this query return?

    ```sql
    SELECT u.name, COUNT(*) AS bookings
    FROM users u
    JOIN bookings b ON b.user_id = u.id
    GROUP BY u.id;
    ```
    """,
    ["5, because the inner join drops Eileen", "6, with Eileen shown as 0",
     "6, with Eileen shown as 1", "10, one for each booking"],
    correct=[0],
    incorrect="Not quite. JOIN on its own is an inner join. What happens to a guest with no matching booking?",
)

MODULE = Module("m05-joins", "Joining Tables", [
    Lesson("l01-inner-joins", "Inner joins", [JOIN_THEORY, TWO, FILTERED, THREE]),
    Lesson("l02-left-joins-and-more", "LEFT JOIN and bigger joins", [NEVER, COUNT_ZERO, FOUR, TAKINGS, FIX, QUIZ]),
])
