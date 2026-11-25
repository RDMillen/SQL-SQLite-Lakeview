Henry Townshend has cancelled booking 10, his stay in January 2027. Delete it.

Booking 10 has an extra attached to it in `booking_extras`. Because of the foreign key, SQLite refuses to delete the booking while that row still points at it. You need two `DELETE` statements, in the right order.

Try the booking first to see the error, then fix the order.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `booking_extras`: `booking_id` (links to `bookings.id`), `extra_id` (links to `extras.id`), `quantity`

Open `lakeview.sql` to see every row.
