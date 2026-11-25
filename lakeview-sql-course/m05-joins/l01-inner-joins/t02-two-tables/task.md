Write a query that shows every booking's `id`, the guest's `name`, and the `check_in` date. Sort by the booking `id`.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `users`: `id`, `name`, `email`, `password_hash`, `phone`

Open `lakeview.sql` to see every row.
