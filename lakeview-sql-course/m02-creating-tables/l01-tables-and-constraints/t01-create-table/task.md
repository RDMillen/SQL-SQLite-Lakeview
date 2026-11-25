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
