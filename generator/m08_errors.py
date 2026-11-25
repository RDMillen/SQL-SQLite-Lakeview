from lib import Lesson, Module
from shared import choice, theory

ERR_THEORY = theory(
    "t01-reading-errors", "Reading SQLite errors",
    """
    SQLite error messages are short, but they nearly always tell you what went wrong and where. Read the whole message before you change anything.

    | Message | What it usually means |
    |---|---|
    | `no such table: room` | the table name is wrong, or the table was never created |
    | `no such column: nmae` | a column name is misspelt, or belongs to a table that is not in the query |
    | `near "FROM": syntax error` | something just before the word in quotes is wrong, often a stray or missing comma |
    | `ambiguous column name: id` | two tables in a join both have this column, so say which one, as in `bookings.id` |
    | `NOT NULL constraint failed: users.email` | a row was given no value for a column that must have one |
    | `UNIQUE constraint failed: users.email` | another row already has this value |
    | `CHECK constraint failed: ...` | the row broke a `CHECK` rule, and the rule is shown after the colon |
    | `FOREIGN KEY constraint failed` | a row points at a parent that does not exist, or a parent still has child rows |

    From Python, the first four come as `sqlite3.OperationalError`, because the SQL itself is wrong. The constraint errors come as `sqlite3.IntegrityError`, because the SQL is fine but the data breaks a rule.

    The quizzes in this lesson show a statement and the error it gave. Pick the fix. Run `examples.sql` to see some of these errors for yourself. `run.py` stops at the first error, so delete each statement once you have seen its error.
    """,
    examples="""
    SELECT nmae FROM users;

    SELECT number, room_type, FROM rooms;

    INSERT INTO users (name, email, password_hash) VALUES ('James again', 'james@example.com', 'demo-hash');
    """,
)


def err(slug, title, statement, message, options, correct, hint):
    return choice(slug, title, f"""
    This statement:

    ```sql
    {statement}
    ```

    gave this error:

    ```text
    {message}
    ```

    What is the fix?
    """, options, correct=[correct], incorrect=hint)


Q1 = err("t02-no-such-column", "no such column",
         "SELECT nmae, email FROM users;", "no such column: nmae",
         ["Spell the column correctly: name",
          "Create a column called nmae in users",
          "Put nmae in single quotes",
          "Turn on foreign keys"], 0,
         "Not quite. Compare the column in the message with the columns in the users table.")

Q2 = err("t03-syntax-error", "syntax error",
         "SELECT number, room_type, FROM rooms;", 'near "FROM": syntax error',
         ["Remove the comma after room_type",
          "Write FROM in lower case",
          "Add a WHERE clause",
          "Put rooms in quotes"], 0,
         "Not quite. The problem is just before the word in quotes. What comes straight before FROM?")

Q3 = err("t04-unique", "UNIQUE constraint failed",
         "INSERT INTO users (name, email, password_hash) VALUES ('James', 'james@example.com', 'demo-hash');",
         "UNIQUE constraint failed: users.email",
         ["Nothing is wrong with the SQL: this email is already registered, so the app should tell the user",
          "Remove UNIQUE from the email column",
          "Leave out the id column",
          "Use UPDATE instead of INSERT"], 0,
         "Not quite. The rule is doing its job. What should the app do when someone registers an email that is already used?")

Q4 = err("t05-foreign-key", "FOREIGN KEY constraint failed",
         "DELETE FROM bookings WHERE id = 1;", "FOREIGN KEY constraint failed",
         ["Delete the booking_extras rows for booking 1 first",
          "Turn foreign keys off and try again",
          "Delete user 1 first",
          "Add LIMIT 1 to the DELETE"], 0,
         "Not quite. Some other table still has rows pointing at booking 1. Which one?")

Q5 = err("t06-ambiguous", "ambiguous column name",
         "SELECT id, name FROM bookings JOIN users ON bookings.user_id = users.id;",
         "ambiguous column name: id",
         ["Say which table's id you mean, for example bookings.id",
          "Rename the id column in one of the tables",
          "Use LEFT JOIN instead of JOIN",
          "Remove the ON part"], 0,
         "Not quite. Both tables have a column called id. How do you tell SQLite which one you want?")

Q6 = err("t07-check", "CHECK constraint failed",
         "INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (401, 'Double', 2, 0);",
         "CHECK constraint failed: price_per_night > 0",
         ["Give the room a price above 0",
          "Leave out the available column",
          "Change the number to 104",
          "Put 0 in single quotes"], 0,
         "Not quite. The rule after the colon is the one that was broken.")

Q7 = err("t08-not-null", "NOT NULL constraint failed",
         "INSERT INTO users (name, password_hash) VALUES ('Maria', 'demo-hash');",
         "NOT NULL constraint failed: users.email",
         ["Include the email column and give it a value",
          "Add NULL to the end of VALUES",
          "Remove the password_hash column",
          "Make email a primary key"], 0,
         "Not quite. The message names the column that was left without a value.")

Q8 = choice(
    "t09-bindings", "Incorrect number of bindings",
    """
    This Python line:

    ```python
    conn.execute("SELECT * FROM users WHERE email = ?", (email))
    ```

    gave this error when `email` was `'mary@example.com'`:

    ```text
    sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 16 supplied.
    ```

    What is the fix?
    """,
    ["Add a comma so the values are a tuple: (email,)",
     "Use an f-string instead of ?",
     "Add 15 more ? placeholders",
     "Put quotes around the ?"],
    correct=[0],
    incorrect="Not quite. (email) is just a string in brackets, so SQLite treats each of its 16 characters as a separate value.",
)

MODULE = Module("m08-reading-errors", "Reading Errors", [
    Lesson("l01-error-messages", "Error messages", [ERR_THEORY, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8]),
])
