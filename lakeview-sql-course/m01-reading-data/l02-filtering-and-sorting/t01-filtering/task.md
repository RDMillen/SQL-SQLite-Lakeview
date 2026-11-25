`WHERE` keeps only the rows that match a condition.

```sql
SELECT number, price_per_night FROM rooms WHERE price_per_night > 100;
```

## Comparison operators

| Operator | Meaning |
|---|---|
| `=` | equal to |
| `<>` or `!=` | not equal to |
| `<`, `<=`, `>`, `>=` | less than, at most, more than, at least |
| `BETWEEN a AND b` | from a to b, including both ends |
| `IN (a, b, c)` | equal to one of the values in the list |
| `LIKE 'pattern'` | text matching a pattern, where `%` means any characters and `_` means one character |
| `IS NULL`, `IS NOT NULL` | the value is missing, or is not missing |

Text goes in single quotes: `'Double'`. Numbers do not: `120`.

Combine conditions with `AND` and `OR`. Use brackets when you mix them, so that SQLite does what you mean.

```sql
SELECT number FROM rooms WHERE available = 1 AND (room_type = 'Double' OR room_type = 'Suite');
```

## Sorting and limiting

`ORDER BY` sorts the rows. Add `DESC` for largest first. You can sort by more than one column: the second column only matters when the first is tied.

```sql
SELECT number, room_type, price_per_night FROM rooms ORDER BY room_type, price_per_night DESC;
```

`LIMIT n` keeps only the first n rows. It goes at the very end. `DISTINCT` removes repeated rows.

```sql
SELECT DISTINCT room_type FROM rooms;
```

## NULL

`NULL` means "no value". In Lakeview, some guests have not given a phone number, so their `phone` is `NULL`. Nothing is ever equal to `NULL`, not even `NULL` itself, so `phone = NULL` never matches anything. Use `phone IS NULL` instead.

Try the queries in `examples.sql` with `run.py`, and change them to see what happens.
