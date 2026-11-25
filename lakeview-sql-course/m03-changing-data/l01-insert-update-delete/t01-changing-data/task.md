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
