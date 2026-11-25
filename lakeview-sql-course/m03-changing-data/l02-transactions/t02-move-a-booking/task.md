Harry Mason wants to move booking 4 from the Suite (room 312) to the Family room (room 201). The dates and number of guests stay the same.

In one transaction:

1. Change the booking's `room_id` to the id of room 201. Look the id up in `rooms`.
2. Change its `total_price` to the new price. Room 201 is 180 a night, there are 2 guests and 3 nights, so the new total is 540.0.

Start with `BEGIN;` and finish with `COMMIT;`.

## Tables you need

- `bookings`: `id`, `user_id` (links to `users.id`), `room_id` (links to `rooms.id`), `check_in`, `check_out`, `occupants`, `total_price`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
