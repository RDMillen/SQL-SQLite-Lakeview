Complete `get_rooms` in `hotel_db.py`. It should run a query and return the `number`, `room_type`, and `price_per_night` of every room, sorted by `number`.

Use `conn.execute(...)` and return the result of `.fetchall()`. Run `hotel_db.py` to see what your function returns.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
