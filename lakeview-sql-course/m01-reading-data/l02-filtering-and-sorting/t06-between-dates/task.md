Dates in Lakeview are stored as text in the form `YYYY-MM-DD`, for example `2026-11-04`. Text in this form sorts in date order, so `<`, `>`, and `BETWEEN` work on it.

Write a query that shows the `id`, `check_in`, and `check_out` of every booking with a `check_in` date in November 2026.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`

Open `lakeview.sql` to see every row.
