Write a query that shows the `name` of every guest who has a booking for the Suite, room number 312. Each guest should appear once. Sort by `name`.

You can use subqueries with `IN`, or a join with `DISTINCT`. Do not type the room's `id`: find it from the room number.

## Tables you need

- `users`: `id`, `name`, `email`, `password_hash`, `phone`
- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
