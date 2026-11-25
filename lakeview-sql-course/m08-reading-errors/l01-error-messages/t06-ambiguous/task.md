This statement:

```sql
SELECT id, name FROM bookings JOIN users ON bookings.user_id = users.id;
```

gave this error:

```text
ambiguous column name: id
```

What is the fix?
