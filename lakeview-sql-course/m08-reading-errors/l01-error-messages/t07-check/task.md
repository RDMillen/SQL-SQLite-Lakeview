This statement:

```sql
INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (401, 'Double', 2, 0);
```

gave this error:

```text
CHECK constraint failed: price_per_night > 0
```

What is the fix?
