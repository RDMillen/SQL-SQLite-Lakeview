Write a query on `bookings` that shows, for each `user_id`:

- the number of bookings, in a column called `bookings`
- the total of their `total_price`, in a column called `spent`

Put the biggest spender first. If two guests have spent the same, put the lower `user_id` first.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`

Open `lakeview.sql` to see every row.
