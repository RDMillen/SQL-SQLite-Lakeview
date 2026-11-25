Write a query that shows every guest's `name` and how many bookings they have, in a column called `bookings`. Guests with no bookings must appear with 0. Sort by `name`.

Think about which table goes on the left of the `LEFT JOIN`, and what you count.

## Tables you need

- `users`: `id`, `name`, `email`, `password_hash`, `phone`
- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`

Open `lakeview.sql` to see every row.
