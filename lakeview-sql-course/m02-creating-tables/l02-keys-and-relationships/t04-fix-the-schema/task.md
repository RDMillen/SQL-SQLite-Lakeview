A colleague wrote a table for housekeeping jobs. It should match this design:

| Column | Type | Rules |
|---|---|---|
| `id` | `INTEGER` | primary key |
| `room_id` | `INTEGER` | must have a value, foreign key to `rooms(id)` |
| `job_date` | `TEXT` | must have a value |
| `minutes` | `INTEGER` | must have a value, and must be more than 0 |

Their SQL has three mistakes. Run it, read the error, fix that mistake, and run it again until the table matches the design.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
