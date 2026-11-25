Aggregate functions turn many rows into one value.

| Function | Gives you |
|---|---|
| `COUNT(*)` | the number of rows |
| `COUNT(column)` | the number of rows where that column is not `NULL` |
| `SUM(column)` | the total |
| `AVG(column)` | the mean |
| `MIN(column)`, `MAX(column)` | the smallest and largest value |

```sql
SELECT COUNT(*) AS bookings, SUM(total_price) AS takings FROM bookings;
```

`AS` gives a column a name. Without it, the column is called `COUNT(*)`, which is awkward to use from Python. `ROUND(value, 2)` rounds to 2 decimal places.

## GROUP BY

`GROUP BY` splits the rows into groups and works out the aggregate once for each group. This query counts the rooms of each type:

```sql
SELECT room_type, COUNT(*) AS rooms
FROM rooms
GROUP BY room_type;
```

Every column after `SELECT` should either be in the `GROUP BY` or be inside an aggregate function. SQLite lets you break this rule and quietly picks a value from somewhere in the group, which gives answers that look right but are not.

## WHERE and HAVING

`WHERE` filters rows before they are grouped. `HAVING` filters the groups afterwards, so it can use aggregates:

```sql
SELECT user_id, COUNT(*) AS bookings
FROM bookings
WHERE check_in >= '2026-12-01'
GROUP BY user_id
HAVING COUNT(*) >= 1;
```

The order of the parts is always `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`.
