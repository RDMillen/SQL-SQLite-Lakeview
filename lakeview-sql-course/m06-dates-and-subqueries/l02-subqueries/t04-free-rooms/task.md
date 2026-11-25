A guest wants a room from `2026-12-01` to `2026-12-03`. Write a query that shows the `number` of every room that:

- is available (`available = 1`)
- has no booking that clashes with those dates

Use `NOT EXISTS` with the clash rule. Sort by `number`.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`
- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`

Open `lakeview.sql` to see every row.
