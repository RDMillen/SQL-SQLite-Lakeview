The front desk wants a booking list. Write a query that shows the guest's `name`, the room `number`, `check_in`, `check_out`, and `total_price` for every booking. Sort by `check_in`, then by room `number`.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `users`: `id`, `name`, `email`, `password_hash`, `phone`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
