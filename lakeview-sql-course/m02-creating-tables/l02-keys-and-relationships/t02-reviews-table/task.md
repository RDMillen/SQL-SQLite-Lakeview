Guests can now leave a review of a room. Write a `CREATE TABLE` statement for a table called `reviews`:

| Column | Type | Rules |
|---|---|---|
| `id` | `INTEGER` | primary key |
| `user_id` | `INTEGER` | must have a value, foreign key to `users(id)` |
| `room_id` | `INTEGER` | must have a value, foreign key to `rooms(id)` |
| `rating` | `INTEGER` | must have a value, from 1 to 5 |
| `comment` | `TEXT` | optional |

## Tables you need

- `users`: `id`, `name`, `email`, `password_hash`, `phone`
- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
