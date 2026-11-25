`ALTER TABLE` changes a table that already has rows in it.

```sql
ALTER TABLE users ADD COLUMN newsletter INTEGER NOT NULL DEFAULT 0;
```

A new column must allow `NULL` or have a `DEFAULT`, because the rows already in the table need a value for it. SQLite can add, rename, and drop columns, but it cannot change the rules on a column that exists. To do that you make a new table and copy the rows across.

Write two statements:

1. Add a column called `floor` to `rooms`. It is an `INTEGER`, must have a value, and is 1 if not given.
2. Update the rooms on other floors. The first digit of the room number is the floor, so room 201 is on floor 2 and room 312 is on floor 3.

Your `UPDATE` should still work if more rooms are added.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
