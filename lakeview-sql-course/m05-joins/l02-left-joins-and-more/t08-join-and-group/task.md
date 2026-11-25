Write a query that shows each `room_type` with the total `total_price` of its bookings, in a column called `takings`. Highest takings first. Room types with no bookings do not need to appear.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
