Write a query that shows, for every extra added to a booking:

- the guest's `name`
- the booking's `check_in`
- the extra's `name`
- the `quantity`

You need four tables. Two of them have a column called `name`, so give the extra's name the alias `extra`. Sort by the guest's name, then `check_in`, then `extra`.

## Tables you need

- `users`: `id`, `name`, `email`, `password_hash`, `phone`
- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `booking_extras`: `booking_id` (links to `bookings.id`), `extra_id` (links to `extras.id`), `quantity`
- `extras`: `id`, `name`, `price`

Open `lakeview.sql` to see every row.
