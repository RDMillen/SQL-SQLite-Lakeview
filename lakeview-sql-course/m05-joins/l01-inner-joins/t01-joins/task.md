A booking row only holds `user_id` and `room_id`. To show the guest's name and the room number, you join `bookings` to `users` and `rooms`.

```sql
SELECT bookings.id, users.name, rooms.number
FROM bookings
JOIN users ON bookings.user_id = users.id
JOIN rooms ON bookings.room_id = rooms.id;
```

`ON` says how the rows match: the foreign key on one side equals the primary key on the other. `JOIN` on its own means `INNER JOIN`. It keeps only the rows that have a match on both sides.

## Table names and aliases

When two tables have a column with the same name, such as `id`, you must say which one you mean: `bookings.id` or `users.id`. If you do not, SQLite gives the error `ambiguous column name: id`.

Typing full table names gets long. An alias is a short name for a table, given straight after it:

```sql
SELECT b.id, u.name, r.number
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN rooms r ON b.room_id = r.id;
```

## LEFT JOIN

`LEFT JOIN` keeps every row from the table on the left, even when there is no match on the right. The columns from the right-hand table are `NULL` for those rows. This is how you find things that have never happened, such as rooms that have never been booked:

```sql
SELECT r.number, b.id
FROM rooms r
LEFT JOIN bookings b ON b.room_id = r.id
WHERE b.id IS NULL;
```

## Joining more tables

Each extra table needs its own `JOIN ... ON`. To get from a guest to the extras on their bookings you follow the keys: `users` to `bookings`, `bookings` to `booking_extras`, `booking_extras` to `extras`. Look at `lakeview.sql` and trace the path before you write the query.

## Joins with GROUP BY

You can group joined rows like any others. `COUNT(b.id)` counts only the rows where a booking was found, so with a `LEFT JOIN` it gives 0 for a guest with no bookings, where `COUNT(*)` would give 1.
