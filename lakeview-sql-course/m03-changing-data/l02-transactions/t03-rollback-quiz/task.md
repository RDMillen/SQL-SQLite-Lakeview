What does this SQL leave in the `extras` table?

```sql
BEGIN;
INSERT INTO extras (name, price) VALUES ('Dinner', 30.0);
UPDATE extras SET price = 0 WHERE name = 'Parking';
ROLLBACK;
```
