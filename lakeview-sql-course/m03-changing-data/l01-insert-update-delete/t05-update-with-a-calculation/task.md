`SET` can use the old value of a column to work out the new one:

```sql
UPDATE rooms SET capacity = capacity + 1 WHERE number = 201;
```

The price of every Double room is going up by 10 percent. Write one `UPDATE` that multiplies `price_per_night` by `1.1` for every room whose `room_type` is `Double`, rounded to 2 decimal places with `ROUND(value, 2)`.

## Tables you need

- `rooms`: `id`, `number`, `room_type`, `capacity`, `price_per_night`, `available`

Open `lakeview.sql` to see every row.
