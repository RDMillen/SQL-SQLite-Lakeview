A subquery is a query inside another query, in brackets. SQLite runs it and uses its result.

## A single value

This finds the rooms that cost more than the average room:

```sql
SELECT number, price_per_night
FROM rooms
WHERE price_per_night > (SELECT AVG(price_per_night) FROM rooms);
```

## A list with IN

A subquery can give a list of values for `IN`. This finds the guests who have booked room id 5:

```sql
SELECT name FROM users
WHERE id IN (SELECT user_id FROM bookings WHERE room_id = 5);
```

## EXISTS and NOT EXISTS

`EXISTS (subquery)` is true when the subquery finds at least one row. `NOT EXISTS` is true when it finds none. The subquery can use columns from the outer query, so it is worked out again for each outer row.

This finds the rooms with no bookings in December:

```sql
SELECT r.number
FROM rooms r
WHERE NOT EXISTS (
    SELECT 1 FROM bookings b
    WHERE b.room_id = r.id
      AND b.check_in BETWEEN '2026-12-01' AND '2026-12-31'
);
```

`SELECT 1` is a habit: `EXISTS` only cares whether a row was found, not what is in it.

Put `NOT EXISTS` together with the clash rule and you have the query behind a "rooms free on these dates" search.
