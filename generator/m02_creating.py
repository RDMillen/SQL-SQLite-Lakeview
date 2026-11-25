from lib import Lesson, Module
from shared import choice, custom_task, state_task, theory

CREATE_THEORY = theory(
    "t01-create-table", "Creating a table",
    """
    `CREATE TABLE` makes a new table. You give each column a name and a type, and you can add rules called constraints.

    ```sql
    CREATE TABLE guests (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        nights_stayed INTEGER NOT NULL DEFAULT 0 CHECK (nights_stayed >= 0)
    );
    ```

    Columns are separated by commas. There is no comma after the last column.

    ## Types in SQLite

    | Type | Use it for | Example |
    |---|---|---|
    | `INTEGER` | whole numbers | `3`, `312` |
    | `REAL` | numbers with a decimal point | `12.5` |
    | `TEXT` | words, emails, dates | `'Breakfast'`, `'2026-11-04'` |
    | `BLOB` | raw data such as images | rarely needed |

    SQLite has no date type. Store dates as `TEXT` in the form `YYYY-MM-DD` so that they sort in the right order.

    SQLite is more relaxed about types than most databases. It will usually store text in an `INTEGER` column if you ask it to. Constraints are how you stop bad data getting in.

    ## Constraints

    | Constraint | What it does |
    |---|---|
    | `PRIMARY KEY` | identifies each row. `INTEGER PRIMARY KEY` also fills in the next number for you when you leave it out of an `INSERT` |
    | `NOT NULL` | the column must have a value |
    | `UNIQUE` | no two rows can have the same value |
    | `DEFAULT value` | the value used when an `INSERT` leaves the column out |
    | `CHECK (condition)` | the row is refused unless the condition is true |

    When a constraint is broken, SQLite refuses the whole statement and gives an error such as `NOT NULL constraint failed: guests.name`.

    The tasks in this lesson start from an empty database, so your table is the only one there. Run `examples.sql` to see the table above being made and used, including an `INSERT` that is refused.
    """,
    examples="""
    CREATE TABLE guests (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        nights_stayed INTEGER NOT NULL DEFAULT 0 CHECK (nights_stayed >= 0)
    );

    INSERT INTO guests (name, email) VALUES ('Maria', 'maria@example.com');

    SELECT * FROM guests;

    -- This one is refused, because the email is already used.
    INSERT INTO guests (name, email) VALUES ('Another Maria', 'maria@example.com');
    """,
    lakeview=False,
)

STAFF = custom_task(
    "t02-staff-table", "A table for staff",
    """
    Lakeview wants to keep a list of its staff. Write a `CREATE TABLE` statement for a table called `staff` with these columns:

    | Column | Type | Rules |
    |---|---|---|
    | `id` | `INTEGER` | primary key |
    | `name` | `TEXT` | must have a value |
    | `role` | `TEXT` | must have a value |
    | `email` | `TEXT` | must have a value, and no two staff can share one |

    This task starts from an empty database. Run `run.py` to check that the table is made, then press Check.
    """,
    ["Create the staff table described in the task."],
    solution="""
    CREATE TABLE staff (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """,
    lakeview=False,
    tests='''
    class TestTask(SQLTestCase):
        def make(self):
            _, statements = self.student_sql()
            conn = new_db(lakeview=False)
            self.run_sql(conn, statements)
            if not table_exists(conn, "staff"):
                self.fail("There is no table called staff yet.")
            return conn

        def test_1_columns(self):
            cols = columns_of(self.make(), "staff")
            for name in ["id", "name", "role", "email"]:
                self.assertIn(name, cols, f"The staff table needs a column called {name}.")
            self.assertEqual(4, len(cols), "The staff table should have exactly 4 columns.")
            self.assertTrue(cols["id"][3], "id should be the PRIMARY KEY.")
            self.assertEqual("INTEGER", cols["id"][0], "id should be INTEGER PRIMARY KEY.")

        def test_2_insert_works(self):
            conn = self.make()
            self.expect_ok(conn, "INSERT INTO staff (name, role, email) VALUES ('Angela', 'Reception', 'angela@example.com')",
                           "A normal INSERT into staff was refused.")
            self.assertEqual(1, conn.execute("SELECT id FROM staff").fetchone()[0],
                             "SQLite should fill in id for you. Check that id is INTEGER PRIMARY KEY.")

        def test_3_not_null(self):
            conn = self.make()
            for column, sql in [
                ("name", "INSERT INTO staff (name, role, email) VALUES (NULL, 'Chef', 'a@example.com')"),
                ("role", "INSERT INTO staff (name, role, email) VALUES ('Eddie', NULL, 'b@example.com')"),
                ("email", "INSERT INTO staff (name, role, email) VALUES ('Eddie', 'Chef', NULL)"),
            ]:
                self.expect_error(conn, sql, f"A member of staff was added with no {column}. Add NOT NULL to {column}.")

        def test_4_unique_email(self):
            conn = self.make()
            conn.execute("INSERT INTO staff (name, role, email) VALUES ('Angela', 'Reception', 'angela@example.com')")
            self.expect_error(conn, "INSERT INTO staff (name, role, email) VALUES ('Eddie', 'Chef', 'angela@example.com')",
                              "Two members of staff were given the same email. Add UNIQUE to email.")
    ''',
    tables=[],
)

PACKAGES = custom_task(
    "t03-check-and-default", "CHECK and DEFAULT",
    """
    Lakeview sells packages such as a lakeside weekend. Write a `CREATE TABLE` statement for a table called `packages`:

    | Column | Type | Rules |
    |---|---|---|
    | `id` | `INTEGER` | primary key |
    | `name` | `TEXT` | must have a value, and must be unique |
    | `price` | `REAL` | must have a value, and cannot be below 0 |
    | `nights` | `INTEGER` | must have a value, must be more than 0, and is 1 if not given |

    You need `CHECK` for the two number rules and `DEFAULT` for the last one.
    """,
    ["Create the packages table described in the task."],
    solution="""
    CREATE TABLE packages (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL CHECK (price >= 0),
        nights INTEGER NOT NULL DEFAULT 1 CHECK (nights > 0)
    );
    """,
    lakeview=False,
    tests='''
    class TestTask(SQLTestCase):
        def make(self):
            _, statements = self.student_sql()
            conn = new_db(lakeview=False)
            self.run_sql(conn, statements)
            if not table_exists(conn, "packages"):
                self.fail("There is no table called packages yet.")
            return conn

        def test_1_columns(self):
            cols = columns_of(self.make(), "packages")
            for name in ["id", "name", "price", "nights"]:
                self.assertIn(name, cols, f"The packages table needs a column called {name}.")
            self.assertTrue(cols["id"][3], "id should be the PRIMARY KEY.")

        def test_2_default_nights(self):
            conn = self.make()
            self.expect_ok(conn, "INSERT INTO packages (name, price) VALUES ('Lakeside weekend', 199.0)",
                           "An INSERT that leaves out nights was refused. Give nights a DEFAULT.")
            self.assertEqual(1, conn.execute("SELECT nights FROM packages").fetchone()[0],
                             "When nights is left out it should be 1. Add DEFAULT 1.")

        def test_3_checks(self):
            conn = self.make()
            self.expect_ok(conn, "INSERT INTO packages (name, price, nights) VALUES ('Free tea', 0, 1)",
                           "A package with a price of 0 was refused, but 0 should be allowed.")
            self.expect_error(conn, "INSERT INTO packages (name, price, nights) VALUES ('Bad', -5, 1)",
                              "A package with a price below 0 was accepted. Add a CHECK on price.")
            self.expect_error(conn, "INSERT INTO packages (name, price, nights) VALUES ('Bad', 10, 0)",
                              "A package with 0 nights was accepted. Add a CHECK on nights.")

        def test_4_not_null_and_unique(self):
            conn = self.make()
            self.expect_error(conn, "INSERT INTO packages (name, price) VALUES (NULL, 10)",
                              "A package with no name was accepted. Add NOT NULL to name.")
            self.expect_error(conn, "INSERT INTO packages (name, price) VALUES ('No price', NULL)",
                              "A package with no price was accepted. Add NOT NULL to price.")
            conn.execute("INSERT INTO packages (name, price) VALUES ('Lakeside weekend', 199)")
            self.expect_error(conn, "INSERT INTO packages (name, price) VALUES ('Lakeside weekend', 99)",
                              "Two packages were given the same name. Add UNIQUE to name.")
    ''',
    tables=[],
)

TYPES_QUIZ = choice(
    "t04-types-quiz", "Quiz: storing dates",
    """
    A new table needs a column for the date a guest arrives. Which column definition fits best in SQLite?
    """,
    ["arrival TEXT NOT NULL, storing values like '2026-11-04'",
     "arrival TEXT NOT NULL, storing values like '04/11/2026'",
     "arrival INTEGER NOT NULL, storing values like 4112026",
     "arrival DATE NOT NULL, because SQLite has a date type"],
    correct=[0],
    incorrect="Not quite. SQLite has no real date type, and dates need to sort in the right order. Which form sorts by year, then month, then day?",
)

FK_THEORY = theory(
    "t01-foreign-keys", "Foreign keys",
    """
    A foreign key is a column that points at the primary key of another table. In Lakeview, `bookings.user_id` points at `users.id`, so every booking belongs to a real guest.

    ```sql
    CREATE TABLE bookings (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        room_id INTEGER NOT NULL REFERENCES rooms(id),
        ...
    );
    ```

    `REFERENCES users(id)` is the foreign key. With it in place, SQLite refuses a booking for a guest who does not exist, and refuses to delete a guest who still has bookings.

    ## Turn foreign keys on

    SQLite only checks foreign keys when you ask it to, once for each connection:

    ```sql
    PRAGMA foreign_keys = ON;
    ```

    `run.py` and the tests in this course always turn it on. In your own Flask project, `get_db()` should run this straight after connecting. If you forget, SQLite stores bookings for guests who do not exist and gives no error. This catches a lot of people out.

    ## ON DELETE

    You can say what happens to the child rows when the parent row is deleted:

    | Option | When a guest is deleted |
    |---|---|
    | (none given) | refused while the guest has bookings |
    | `ON DELETE CASCADE` | their bookings are deleted too |
    | `ON DELETE SET NULL` | their bookings stay, with `user_id` set to `NULL` |

    ## Many-to-many relationships

    One booking can have many extras, and one extra can be on many bookings. A table in the middle, often called a junction or link table, holds one row for each pairing. In Lakeview this is `booking_extras`:

    ```sql
    CREATE TABLE booking_extras (
        booking_id INTEGER NOT NULL REFERENCES bookings(id),
        extra_id INTEGER NOT NULL REFERENCES extras(id),
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        PRIMARY KEY (booking_id, extra_id)
    );
    ```

    The primary key is made of both columns together, so the same extra cannot be added to the same booking twice. This is called a composite key.

    The tasks in this lesson run on the full Lakeview database, so your new tables can point at `users`, `rooms`, and the rest. Run `examples.sql` to see a foreign key refuse a row.
    """,
    examples="""
    -- Guest 99 does not exist, so this is refused.
    INSERT INTO bookings (user_id, room_id, check_in, check_out, occupants, total_price)
    VALUES (99, 1, '2027-02-01', '2027-02-02', 1, 80.0);
    """,
)

REVIEWS = custom_task(
    "t02-reviews-table", "A reviews table",
    """
    Guests can now leave a review of a room. Write a `CREATE TABLE` statement for a table called `reviews`:

    | Column | Type | Rules |
    |---|---|---|
    | `id` | `INTEGER` | primary key |
    | `user_id` | `INTEGER` | must have a value, foreign key to `users(id)` |
    | `room_id` | `INTEGER` | must have a value, foreign key to `rooms(id)` |
    | `rating` | `INTEGER` | must have a value, from 1 to 5 |
    | `comment` | `TEXT` | optional |
    """,
    ["Create the reviews table described in the task.",
     "This task runs on the full Lakeview database."],
    solution="""
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        room_id INTEGER NOT NULL REFERENCES rooms(id),
        rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
        comment TEXT
    );
    """,
    tests='''
    class TestTask(SQLTestCase):
        def make(self):
            _, statements = self.student_sql()
            conn = new_db()
            self.run_sql(conn, statements)
            if not table_exists(conn, "reviews"):
                self.fail("There is no table called reviews yet.")
            return conn

        def test_1_columns(self):
            cols = columns_of(self.make(), "reviews")
            for name in ["id", "user_id", "room_id", "rating", "comment"]:
                self.assertIn(name, cols, f"The reviews table needs a column called {name}.")
            self.assertTrue(cols["id"][3], "id should be the PRIMARY KEY.")

        def test_2_foreign_keys(self):
            fks = foreign_keys_of(self.make(), "reviews")
            pairs = {(f[0], f[1]) for f in fks}
            self.assertIn(("user_id", "users"), pairs, "user_id should be a foreign key: REFERENCES users(id).")
            self.assertIn(("room_id", "rooms"), pairs, "room_id should be a foreign key: REFERENCES rooms(id).")

        def test_3_rows(self):
            conn = self.make()
            self.expect_ok(conn, "INSERT INTO reviews (user_id, room_id, rating) VALUES (1, 1, 5)",
                           "A review with no comment was refused. comment should be optional.")
            self.expect_error(conn, "INSERT INTO reviews (user_id, room_id, rating) VALUES (99, 1, 4)",
                              "A review from guest 99, who does not exist, was accepted.")
            self.expect_error(conn, "INSERT INTO reviews (user_id, room_id, rating) VALUES (1, 99, 4)",
                              "A review of room id 99, which does not exist, was accepted.")
            self.expect_error(conn, "INSERT INTO reviews (user_id, room_id, rating) VALUES (1, 1, NULL)",
                              "A review with no rating was accepted. Add NOT NULL to rating.")

        def test_4_rating_range(self):
            conn = self.make()
            self.expect_ok(conn, "INSERT INTO reviews (user_id, room_id, rating) VALUES (1, 1, 1)",
                           "A rating of 1 was refused, but 1 to 5 should be allowed.")
            for bad in (0, 6):
                self.expect_error(conn, f"INSERT INTO reviews (user_id, room_id, rating) VALUES (1, 1, {bad})",
                                  f"A rating of {bad} was accepted. Ratings must be from 1 to 5.")
    ''',
    tables=['users', 'rooms'],
)

FEATURES = custom_task(
    "t03-junction-table", "A many-to-many relationship",
    """
    Rooms have features such as a lake view or a bath. One room can have many features, and one feature can belong to many rooms. Write two `CREATE TABLE` statements.

    `features`:

    | Column | Type | Rules |
    |---|---|---|
    | `id` | `INTEGER` | primary key |
    | `name` | `TEXT` | must have a value, and must be unique |

    `room_features`, the junction table:

    | Column | Type | Rules |
    |---|---|---|
    | `room_id` | `INTEGER` | must have a value, foreign key to `rooms(id)` |
    | `feature_id` | `INTEGER` | must have a value, foreign key to `features(id)` |

    The primary key of `room_features` is both columns together.

    Create `features` first. A table can only point at a table that already exists when rows are added.
    """,
    ["Create the features and room_features tables described in the task."],
    solution="""
    CREATE TABLE features (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE room_features (
        room_id INTEGER NOT NULL REFERENCES rooms(id),
        feature_id INTEGER NOT NULL REFERENCES features(id),
        PRIMARY KEY (room_id, feature_id)
    );
    """,
    tests='''
    class TestTask(SQLTestCase):
        def make(self):
            _, statements = self.student_sql()
            conn = new_db()
            self.run_sql(conn, statements)
            for table in ("features", "room_features"):
                if not table_exists(conn, table):
                    self.fail(f"There is no table called {table} yet.")
            return conn

        def test_1_features(self):
            conn = self.make()
            cols = columns_of(conn, "features")
            self.assertIn("name", cols, "features needs a column called name.")
            self.expect_ok(conn, "INSERT INTO features (name) VALUES ('Lake view')", "Adding a feature was refused.")
            self.expect_error(conn, "INSERT INTO features (name) VALUES ('Lake view')",
                              "The same feature name was added twice. Add UNIQUE to name.")

        def test_2_composite_key(self):
            cols = columns_of(self.make(), "room_features")
            for name in ("room_id", "feature_id"):
                self.assertIn(name, cols, f"room_features needs a column called {name}.")
            self.assertTrue(cols["room_id"][3] and cols["feature_id"][3],
                            "The primary key of room_features should be both columns: PRIMARY KEY (room_id, feature_id).")

        def test_3_foreign_keys(self):
            pairs = {(f[0], f[1]) for f in foreign_keys_of(self.make(), "room_features")}
            self.assertIn(("room_id", "rooms"), pairs, "room_id should be a foreign key: REFERENCES rooms(id).")
            self.assertIn(("feature_id", "features"), pairs, "feature_id should be a foreign key: REFERENCES features(id).")

        def test_4_rows(self):
            conn = self.make()
            conn.execute("INSERT INTO features (id, name) VALUES (1, 'Lake view')")
            self.expect_ok(conn, "INSERT INTO room_features (room_id, feature_id) VALUES (5, 1)",
                           "Linking room id 5 to feature 1 was refused.")
            self.expect_ok(conn, "INSERT INTO room_features (room_id, feature_id) VALUES (4, 1)",
                           "Linking a second room to the same feature was refused.")
            self.expect_error(conn, "INSERT INTO room_features (room_id, feature_id) VALUES (5, 1)",
                              "The same room and feature were linked twice.")
            self.expect_error(conn, "INSERT INTO room_features (room_id, feature_id) VALUES (99, 1)",
                              "Room id 99 does not exist, but it was linked to a feature.")
    ''',
    tables=['rooms'],
)

FIX_SCHEMA = custom_task(
    "t04-fix-the-schema", "Fix the schema",
    """
    A colleague wrote a table for housekeeping jobs. It should match this design:

    | Column | Type | Rules |
    |---|---|---|
    | `id` | `INTEGER` | primary key |
    | `room_id` | `INTEGER` | must have a value, foreign key to `rooms(id)` |
    | `job_date` | `TEXT` | must have a value |
    | `minutes` | `INTEGER` | must have a value, and must be more than 0 |

    Their SQL has three mistakes. Run it, read the error, fix that mistake, and run it again until the table matches the design.
    """,
    ["This should create the cleaning_jobs table from the design in the task.",
     "It has three mistakes."],
    solution="""
    CREATE TABLE cleaning_jobs (
        id INTEGER PRIMARY KEY,
        room_id INTEGER NOT NULL REFERENCES rooms(id),
        job_date TEXT NOT NULL,
        minutes INTEGER NOT NULL CHECK (minutes > 0)
    );
    """,
    placeholder="""
    CREATE TABLE cleaning_jobs (
        id INTEGER PRIMARY KEY,
        room_id INTEGER NOT NULL REFERENCES room(id)
        job_date TEXT NOT NULL,
        minutes INTEGER CHECK (minutes > 0)
    );
    """,
    tests='''
    class TestTask(SQLTestCase):
        def make(self):
            _, statements = self.student_sql()
            conn = new_db()
            self.run_sql(conn, statements)
            if not table_exists(conn, "cleaning_jobs"):
                self.fail("There is no table called cleaning_jobs yet.")
            return conn

        def test_1_foreign_key(self):
            conn = self.make()
            self.expect_ok(conn, "INSERT INTO cleaning_jobs (room_id, job_date, minutes) VALUES (1, '2026-11-04', 30)",
                           "A normal cleaning job for room id 1 was refused. Check which table room_id points at.")
            self.expect_error(conn, "INSERT INTO cleaning_jobs (room_id, job_date, minutes) VALUES (99, '2026-11-04', 30)",
                              "A job for room id 99, which does not exist, was accepted.")

        def test_2_minutes(self):
            conn = self.make()
            self.expect_error(conn, "INSERT INTO cleaning_jobs (room_id, job_date, minutes) VALUES (1, '2026-11-04', NULL)",
                              "A job with no minutes was accepted. minutes must have a value.")
            self.expect_error(conn, "INSERT INTO cleaning_jobs (room_id, job_date, minutes) VALUES (1, '2026-11-04', 0)",
                              "A job of 0 minutes was accepted.")
    ''',
    tables=['rooms'],
)

ALTER = state_task(
    "t05-alter-table", "Adding a column",
    """
    `ALTER TABLE` changes a table that already has rows in it.

    ```sql
    ALTER TABLE users ADD COLUMN newsletter INTEGER NOT NULL DEFAULT 0;
    ```

    A new column must allow `NULL` or have a `DEFAULT`, because the rows already in the table need a value for it. SQLite can add, rename, and drop columns, but it cannot change the rules on a column that exists. To do that you make a new table and copy the rows across.

    Write two statements:

    1. Add a column called `floor` to `rooms`. It is an `INTEGER`, must have a value, and is 1 if not given.
    2. Update the rooms on other floors. The first digit of the room number is the floor, so room 201 is on floor 2 and room 312 is on floor 3.

    Your `UPDATE` should still work if more rooms are added.
    """,
    ["1. Add the floor column to rooms.",
     "2. Set the floor of every room from the first digit of its number."],
    solution="""
    ALTER TABLE rooms ADD COLUMN floor INTEGER NOT NULL DEFAULT 1;

    UPDATE rooms SET floor = number / 100;
    """,
    probes=[("SELECT number, floor FROM rooms ORDER BY number", "the floor of each room")],
    must_use=["ALTER TABLE"],
    tables=['rooms'],
)

FK_QUIZ = choice(
    "t06-foreign-key-quiz", "Quiz: the missing error",
    """
    A student's Flask app saves a booking for `user_id` 42. There is no user with id 42, and the `bookings` table has `REFERENCES users(id)`. SQLite gives no error and the booking is saved.

    What is the most likely cause?
    """,
    ["The app never ran PRAGMA foreign_keys = ON on its connection.",
     "user_id should have been declared as TEXT.",
     "Foreign keys only work on columns called id.",
     "The booking needs a CHECK constraint as well."],
    correct=[0],
    incorrect="Not quite. SQLite does not check foreign keys unless it is told to, once for each connection.",
)

MODULE = Module("m02-creating-tables", "Creating Tables", [
    Lesson("l01-tables-and-constraints", "Tables and constraints", [CREATE_THEORY, STAFF, PACKAGES, TYPES_QUIZ]),
    Lesson("l02-keys-and-relationships", "Keys and relationships",
           [FK_THEORY, REVIEWS, FEATURES, FIX_SCHEMA, ALTER, FK_QUIZ]),
])
