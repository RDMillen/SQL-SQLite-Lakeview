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
