from lib import Lesson, Module
from shared import choice, state_task, theory

USERS = ("SELECT id, name, email, password_hash, phone FROM users ORDER BY id", "the users table")
ROOMS = ("SELECT id, number, room_type, capacity, price_per_night, available FROM rooms ORDER BY id", "the rooms table")
BOOKINGS = ("SELECT * FROM bookings ORDER BY id", "the bookings table")
EXTRAS = ("SELECT name, price FROM extras ORDER BY name", "the extras table")
BOOKING_EXTRAS = ("SELECT * FROM booking_extras ORDER BY booking_id, extra_id", "the booking_extras table")

DML_THEORY = theory(
    "t01-changing-data", "INSERT, UPDATE, and DELETE",
    """
    ## INSERT

    `INSERT` adds rows. Always list the columns you are filling in. Columns you leave out get their `DEFAULT`, or `NULL`, and an `INTEGER PRIMARY KEY` gets the next number.

    ```sql
    INSERT INTO extras (name, price) VALUES ('Dinner', 30.0);
    ```

    You can add several rows in one statement by separating the brackets with commas:

    ```sql
    INSERT INTO extras (name, price) VALUES
        ('Dinner', 30.0),
        ('Spa pass', 22.5);
    ```

    ## UPDATE

    `UPDATE` changes rows that already exist. `SET` gives the new values and `WHERE` picks the rows.

    ```sql
    UPDATE rooms SET price_per_night = 90.0 WHERE number = 101;
    ```

    An `UPDATE` without `WHERE` changes every row in the table. There is no undo button. Before you run an `UPDATE` or `DELETE`, write it as a `SELECT` with the same `WHERE` and check that it picks only the rows you mean.

    ## DELETE

    `DELETE` removes rows. The same warning applies: no `WHERE` means every row goes.

    ```sql
    DELETE FROM extras WHERE name = 'Dinner';
    ```

    If other rows point at a row through a foreign key, SQLite refuses to delete it. Delete the child rows first, or use `ON DELETE CASCADE` in the table design.

    ## Checking your work

    In these tasks you can add a `SELECT` at the end of `task.sql` to see the result when you run `run.py`. The tests ignore it. Every run starts from a fresh copy of the database, so you can run your changes as many times as you like.
    """,
    examples="""
    INSERT INTO extras (name, price) VALUES ('Dinner', 30.0);

    UPDATE extras SET price = 32.0 WHERE name = 'Dinner';

    SELECT * FROM extras;

    DELETE FROM extras WHERE name = 'Dinner';

    SELECT * FROM extras;
    """,
)

INSERT_ONE = state_task(
    "t02-insert-a-row", "Adding a guest",
    """
    Maria has signed up for an account. Write an `INSERT` that adds her to `users` with:

    - `name`: `Maria`
    - `email`: `maria@example.com`
    - `password_hash`: `demo-hash`

    She has not given a phone number. Let SQLite fill in the `id`.
    """,
    ["Add Maria to the users table."],
    solution="INSERT INTO users (name, email, password_hash) VALUES ('Maria', 'maria@example.com', 'demo-hash');",
    probes=[USERS],
    must_use=["INSERT INTO"],
    tables=['users'],
)

INSERT_MANY = state_task(
    "t03-insert-several-rows", "Adding several rows at once",
    """
    The hotel is adding two new extras. Add both in a single `INSERT` statement:

    | name | price |
    |---|---|
    | `Dinner` | 30.0 |
    | `Spa pass` | 22.5 |
    """,
    ["Add both new extras in one INSERT statement."],
    solution="""
    INSERT INTO extras (name, price) VALUES
        ('Dinner', 30.0),
        ('Spa pass', 22.5);
    """,
    probes=[EXTRAS],
    must_use=["INSERT INTO"],
    tables=['extras'],
)

UPDATE_ONE = state_task(
    "t04-update", "Room 102 is back",
    """
    Room 102 has been redecorated and can be booked again. Write an `UPDATE` that sets its `available` value to `1`.

    Pick the room by its `number`, not its `id`. Only room 102 should change.
    """,
    ["Make room 102 available again."],
    solution="UPDATE rooms SET available = 1 WHERE number = 102;",
    probes=[ROOMS],
    must_use=["UPDATE", "WHERE"],
    tables=['rooms'],
)

UPDATE_CALC = state_task(
    "t05-update-with-a-calculation", "A price rise",
    """
    `SET` can use the old value of a column to work out the new one:

    ```sql
    UPDATE rooms SET capacity = capacity + 1 WHERE number = 201;
    ```

    The price of every Double room is going up by 10 percent. Write one `UPDATE` that multiplies `price_per_night` by `1.1` for every room whose `room_type` is `Double`, rounded to 2 decimal places with `ROUND(value, 2)`.
    """,
    ["Raise the price of every Double room by 10 percent, rounded to 2 decimal places."],
    solution="UPDATE rooms SET price_per_night = ROUND(price_per_night * 1.1, 2) WHERE room_type = 'Double';",
    probes=[ROOMS],
    must_use=["UPDATE", "WHERE"],
    tables=['rooms'],
)

DELETE_ORDER = state_task(
    "t06-delete-in-the-right-order", "Cancelling a booking",
    """
    Henry Townshend has cancelled booking 10, his stay in January 2027. Delete it.

    Booking 10 has an extra attached to it in `booking_extras`. Because of the foreign key, SQLite refuses to delete the booking while that row still points at it. You need two `DELETE` statements, in the right order.

    Try the booking first to see the error, then fix the order.
    """,
    ["Delete booking 10 and the booking_extras rows that belong to it."],
    solution="""
    DELETE FROM booking_extras WHERE booking_id = 10;

    DELETE FROM bookings WHERE id = 10;
    """,
    probes=[BOOKINGS, BOOKING_EXTRAS],
    must_use=["DELETE", "WHERE"],
    tables=['bookings', 'booking_extras'],
)

FIX_UPDATE = state_task(
    "t07-fix-the-update", "Fix the dangerous UPDATE",
    """
    Eileen Galvin has given her phone number, `07700 900006`. A colleague wrote the `UPDATE` below to save it.

    Run it with a `SELECT * FROM users;` underneath and look at every guest's phone number. Then fix it so that only Eileen changes. Pick her by her email, `eileen@example.com`, because two guests could share a name.
    """,
    ["This should save Eileen's phone number. Fix it so that only Eileen changes."],
    solution="UPDATE users SET phone = '07700 900006' WHERE email = 'eileen@example.com';",
    placeholder="UPDATE users SET phone = '07700 900006';",
    probes=[USERS],
    tables=['users'],
)

TX_THEORY = theory(
    "t01-transactions", "Transactions",
    """
    Some changes only make sense together. Moving a booking to a new room means changing the room and the price. If the first change worked and the second failed, the booking would be wrong.

    A transaction groups statements so that they all happen or none do.

    ```sql
    BEGIN;
    UPDATE bookings SET room_id = 4 WHERE id = 4;
    UPDATE bookings SET total_price = 540.0 WHERE id = 4;
    COMMIT;
    ```

    `COMMIT` saves everything since `BEGIN`. `ROLLBACK` throws it all away instead, as if none of it had happened.

    Until you `COMMIT`, other connections to the database do not see your changes. In Python, `sqlite3` starts a transaction for you before an `INSERT`, `UPDATE`, or `DELETE`, which is why your Flask code must call `db.commit()` or the change is lost when the request ends.

    Run `examples.sql`. It makes a change inside a transaction, rolls it back, and shows that nothing changed.
    """,
    examples="""
    BEGIN;
    DELETE FROM booking_extras;
    SELECT COUNT(*) AS rows_inside_transaction FROM booking_extras;
    ROLLBACK;

    SELECT COUNT(*) AS rows_after_rollback FROM booking_extras;
    """,
)

TX_TASK = state_task(
    "t02-move-a-booking", "Moving a booking",
    """
    Harry Mason wants to move booking 4 from the Suite (room 312) to the Family room (room 201). The dates and number of guests stay the same.

    In one transaction:

    1. Change the booking's `room_id` to the id of room 201. Look the id up in `rooms`.
    2. Change its `total_price` to the new price. Room 201 is 180 a night, there are 2 guests and 3 nights, so the new total is 540.0.

    Start with `BEGIN;` and finish with `COMMIT;`.
    """,
    ["Move booking 4 to room 201 and update its price, inside one transaction."],
    solution="""
    BEGIN;
    UPDATE bookings SET room_id = 4 WHERE id = 4;
    UPDATE bookings SET total_price = 540.0 WHERE id = 4;
    COMMIT;
    """,
    probes=[BOOKINGS],
    must_use=["BEGIN", "COMMIT"],
    tables=['bookings', 'rooms'],
)

TX_QUIZ = choice(
    "t03-rollback-quiz", "Quiz: ROLLBACK",
    """
    What does this SQL leave in the `extras` table?

    ```sql
    BEGIN;
    INSERT INTO extras (name, price) VALUES ('Dinner', 30.0);
    UPDATE extras SET price = 0 WHERE name = 'Parking';
    ROLLBACK;
    ```
    """,
    ["The four original extras, with Parking still at 8.0",
     "Five extras, with Parking at 0",
     "Five extras, with Parking still at 8.0",
     "No extras at all"],
    correct=[0],
    incorrect="Not quite. ROLLBACK undoes every change made since BEGIN.",
)

MODULE = Module("m03-changing-data", "Changing Data", [
    Lesson("l01-insert-update-delete", "INSERT, UPDATE, and DELETE",
           [DML_THEORY, INSERT_ONE, INSERT_MANY, UPDATE_ONE, UPDATE_CALC, DELETE_ORDER, FIX_UPDATE]),
    Lesson("l02-transactions", "Transactions", [TX_THEORY, TX_TASK, TX_QUIZ]),
])
