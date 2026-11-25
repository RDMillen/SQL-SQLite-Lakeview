A guest asks for room 101 from `2026-11-03` to `2026-11-05`. Write a query that shows the `id`, `check_in`, and `check_out` of every existing booking of room 101 that clashes with this stay.

Use the clash rule from the start of this lesson. Room 101 has `id` 1 in the `rooms` table.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
