`LIKE` matches text against a pattern. `%` stands for any number of characters, including none.

```sql
SELECT name FROM users WHERE name LIKE 'J%';
```

Write a query that shows the `name` and `email` of every guest whose surname is Mason. The surname is the last word in `name`.

## Tables you need

- `users`: `id`, `name`, `email`, `password_hash`, `phone`

Open `lakeview.sql` to see every row.
