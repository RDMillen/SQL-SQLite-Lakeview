This query should show each booking's `id`, the guest's `name`, and the room `number`, sorted by booking `id`. Run it and read the error. Then fix it.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `users`: `id`, `name`, `email`, `password_hash`, `phone`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
