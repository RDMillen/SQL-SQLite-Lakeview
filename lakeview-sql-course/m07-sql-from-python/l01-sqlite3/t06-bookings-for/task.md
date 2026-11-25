Complete `bookings_for`. Given a guest's email, it returns a list of their bookings, sorted by `check_in`. Each booking is a dictionary with the keys `number` (the room number), `check_in` and `check_out`.

You need to join `bookings`, `users`, and `rooms`. Because the connection uses `sqlite3.Row`, `dict(row)` turns each row into a dictionary with the column names as keys.

A guest with no bookings gives an empty list.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `users`: `id`, `name`, `email`, `password_hash`, `phone`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
