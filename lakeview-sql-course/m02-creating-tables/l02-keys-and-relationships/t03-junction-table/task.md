Rooms have features such as a lake view or a bath. One room can have many features, and one feature can belong to many rooms. Write two `CREATE TABLE` statements.

`features`:

| Column | Type | Rules |
|---|---|---|
| `id` | `INTEGER` | primary key |
| `name` | `TEXT` | must have a value, and must be unique |

`room_features`, the junction table:

| Column | Type | Rules |
|---|---|---|
| `room_id` | `INTEGER` | must have a value, foreign key to `rooms(id)` |
| `feature_id` | `INTEGER` | must have a value, foreign key to `features(id)` |

The primary key of `room_features` is both columns together.

Create `features` first. A table can only point at a table that already exists when rows are added.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
