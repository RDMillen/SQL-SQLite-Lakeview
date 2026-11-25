from lib import Lesson, Module
from shared import choice, select_task, theory

AGG_THEORY = theory(
    "t01-aggregates", "Counting and totals",
    """
    Aggregate functions turn many rows into one value.

    | Function | Gives you |
    |---|---|
    | `COUNT(*)` | the number of rows |
    | `COUNT(column)` | the number of rows where that column is not `NULL` |
    | `SUM(column)` | the total |
    | `AVG(column)` | the mean |
    | `MIN(column)`, `MAX(column)` | the smallest and largest value |

    ```sql
    SELECT COUNT(*) AS bookings, SUM(total_price) AS takings FROM bookings;
    ```

    `AS` gives a column a name. Without it, the column is called `COUNT(*)`, which is awkward to use from Python. `ROUND(value, 2)` rounds to 2 decimal places.

    ## GROUP BY

    `GROUP BY` splits the rows into groups and works out the aggregate once for each group. This query counts the rooms of each type:

    ```sql
    SELECT room_type, COUNT(*) AS rooms
    FROM rooms
    GROUP BY room_type;
    ```

    Every column after `SELECT` should either be in the `GROUP BY` or be inside an aggregate function. SQLite lets you break this rule and quietly picks a value from somewhere in the group, which gives answers that look right but are not.

    ## WHERE and HAVING

    `WHERE` filters rows before they are grouped. `HAVING` filters the groups afterwards, so it can use aggregates:

    ```sql
    SELECT user_id, COUNT(*) AS bookings
    FROM bookings
    WHERE check_in >= '2026-12-01'
    GROUP BY user_id
    HAVING COUNT(*) >= 1;
    ```

    The order of the parts is always `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`.
    """,
    examples="""
    SELECT COUNT(*) AS bookings, SUM(total_price) AS takings FROM bookings;

    SELECT room_type, COUNT(*) AS rooms FROM rooms GROUP BY room_type;

    SELECT user_id, COUNT(*) AS bookings
    FROM bookings
    WHERE check_in >= '2026-12-01'
    GROUP BY user_id
    HAVING COUNT(*) >= 1;
    """,
)

COUNT = select_task(
    "t02-count", "How many guests?",
    """
    Write a query that counts the rows in `users`. Name the column `guests`.
    """,
    ["Count the guests in the users table. Name the column guests."],
    solution="SELECT COUNT(*) AS guests FROM users;",
    names=True, must_use=["COUNT"],
    tables=['users'],
)

SUM = select_task(
    "t03-sum", "Total takings",
    """
    Write a query that adds up the `total_price` of every booking. Name the column `takings`.
    """,
    ["Add up total_price for every booking. Name the column takings."],
    solution="SELECT SUM(total_price) AS takings FROM bookings;",
    names=True, must_use=["SUM"],
    tables=['bookings'],
)

AVG = select_task(
    "t04-avg-and-round", "Average price per night",
    """
    Write a query that shows the average `price_per_night` of the rooms that are available, rounded to 2 decimal places. Name the column `average_price`.
    """,
    ["Show the average price_per_night of available rooms, rounded to 2 decimal places.",
     "Name the column average_price."],
    solution="SELECT ROUND(AVG(price_per_night), 2) AS average_price FROM rooms WHERE available = 1;",
    names=True, must_use=["AVG", "ROUND"],
    tables=['rooms'],
)

GROUP = select_task(
    "t05-group-by", "Rooms of each type",
    """
    Write a query that shows each `room_type` with the number of rooms of that type, in a column called `rooms`. Sort by `room_type` from A to Z.
    """,
    ["Show each room_type and how many rooms there are of that type.",
     "Name the count rooms. Sort by room_type."],
    solution="SELECT room_type, COUNT(*) AS rooms FROM rooms GROUP BY room_type ORDER BY room_type;",
    names=True, ordered=True, must_use=["GROUP BY"],
    tables=['rooms'],
)

SPEND = select_task(
    "t06-spend-per-guest", "Spend per guest",
    """
    Write a query on `bookings` that shows, for each `user_id`:

    - the number of bookings, in a column called `bookings`
    - the total of their `total_price`, in a column called `spent`

    Put the biggest spender first. If two guests have spent the same, put the lower `user_id` first.
    """,
    ["For each user_id, show the number of bookings and the total spent.",
     "Biggest spender first, then lower user_id first."],
    solution="""
    SELECT user_id, COUNT(*) AS bookings, SUM(total_price) AS spent
    FROM bookings
    GROUP BY user_id
    ORDER BY spent DESC, user_id;
    """,
    names=True, ordered=True, must_use=["GROUP BY"],
    tables=['bookings'],
)

HAVING = select_task(
    "t07-having", "Regular guests",
    """
    Write a query that shows the `user_id` of every guest with more than one booking, and how many bookings they have in a column called `bookings`. Sort by `user_id`.
    """,
    ["Show the user_id and number of bookings of guests with more than one booking.",
     "Name the count bookings. Sort by user_id."],
    solution="""
    SELECT user_id, COUNT(*) AS bookings
    FROM bookings
    GROUP BY user_id
    HAVING COUNT(*) > 1
    ORDER BY user_id;
    """,
    names=True, ordered=True, must_use=["GROUP BY", "HAVING"],
    tables=['bookings'],
)

QUIZ = choice(
    "t08-where-or-having", "Quiz: WHERE or HAVING",
    """
    You want each room type whose average price is over 150. Which query is right?
    """,
    ["SELECT room_type FROM rooms GROUP BY room_type HAVING AVG(price_per_night) > 150;",
     "SELECT room_type FROM rooms WHERE AVG(price_per_night) > 150 GROUP BY room_type;",
     "SELECT room_type FROM rooms WHERE price_per_night > 150;",
     "SELECT room_type FROM rooms HAVING price_per_night > 150 GROUP BY room_type;"],
    correct=[0],
    incorrect="Not quite. WHERE works on single rows before grouping, so it cannot use AVG. Which part filters whole groups?",
)

MODULE = Module("m04-aggregates", "Counting and Grouping", [
    Lesson("l01-aggregates", "Aggregates and GROUP BY", [AGG_THEORY, COUNT, SUM, AVG, GROUP, SPEND, HAVING, QUIZ]),
])
