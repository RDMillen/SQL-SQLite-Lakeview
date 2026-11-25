There are 6 guests. Eileen Galvin has no bookings. How many rows does this query return?

```sql
SELECT u.name, COUNT(*) AS bookings
FROM users u
JOIN bookings b ON b.user_id = u.id
GROUP BY u.id;
```
