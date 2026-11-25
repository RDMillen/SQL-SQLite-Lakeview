Lakeview stores dates as text in the form `YYYY-MM-DD`. SQLite has functions that understand this form.

| Expression | Result |
|---|---|
| `date('2026-11-01', '+3 days')` | `2026-11-04` |
| `date('2026-11-30', '+1 month')` | `2026-12-30` |
| `date('now')` | today's date |
| `julianday('2026-11-04') - julianday('2026-11-01')` | `3.0` |

`julianday` turns a date into a number of days, so subtracting two of them gives the number of nights between check-in and check-out. The result is a `REAL`. Wrap it in `CAST(... AS INTEGER)` to get a whole number.

```sql
SELECT id, CAST(julianday(check_out) - julianday(check_in) AS INTEGER) AS nights
FROM bookings;
```

Because the dates are in `YYYY-MM-DD` form, comparing them as text also compares them as dates: `'2026-11-04' < '2026-12-01'` is true. This only works if every date is stored the same way, with leading zeros.

## When do two stays clash?

A room cannot be booked by two people on the same night. A new stay from `new_in` to `new_out` clashes with an existing stay when both of these are true:

```text
new_in < existing_out
new_out > existing_in
```

The check-out day is not a night in the room, so back-to-back stays are fine. James checks out of room 101 on 4 November and Heather checks in on 4 November, and there is no clash.

Here is the night-by-night picture for room 101 in early November. Each column is a night, starting on that date.

```text
Night of          1   2   3   4   5   6
James  1 to 4     X   X   X
Heather 4 to 7                X   X   X
New    3 to 5             ?   ?
```

The new stay wants the nights of the 3rd and the 4th. James has the 3rd and Heather has the 4th, so it clashes with both.
