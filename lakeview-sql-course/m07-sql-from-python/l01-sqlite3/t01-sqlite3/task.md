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
