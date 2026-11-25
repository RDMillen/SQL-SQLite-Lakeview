`SELECT` reads rows from a table. The star means every column.

```sql
SELECT * FROM users;
```

In `task.sql`, replace the word `table_name` so that the query shows every column of every row in the `bookings` table.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`

Open `lakeview.sql` to see every row.
