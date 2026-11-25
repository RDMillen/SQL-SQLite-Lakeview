Complete `find_room`. It should return the `number`, `room_type`, and `price_per_night` of the room with the given `number`, or `None` if there is no such room.

Use a `?` placeholder for the number and pass `(number,)` as the second argument to `execute`. Then use `.fetchone()`, which gives `None` when no row matches.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
