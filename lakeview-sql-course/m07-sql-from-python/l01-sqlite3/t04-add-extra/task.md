Complete `add_extra`. It should:

1. insert a row into `extras` with the given `name` and `price`, using `?` placeholders
2. call `conn.commit()`
3. return the new row's id, from `cursor.lastrowid`

The tests check that the row is saved by opening a second connection to the same database file. Without `commit()`, the second connection cannot see it.

## Tables you need

- `extras`: `id`, `name`, `price`

Open `lakeview.sql` to see every row.
