Write a query that shows the `number` of every room that has no bookings at all. Use a `LEFT JOIN`.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`
- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`

Open `lakeview.sql` to see every row.
