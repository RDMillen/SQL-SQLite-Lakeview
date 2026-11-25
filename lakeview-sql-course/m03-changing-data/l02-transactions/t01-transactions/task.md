Some changes only make sense together. Moving a booking to a new room means changing the room and the price. If the first change worked and the second failed, the booking would be wrong.

A transaction groups statements so that they all happen or none do.

```sql
BEGIN;
UPDATE bookings SET room_id = 4 WHERE id = 4;
UPDATE bookings SET total_price = 540.0 WHERE id = 4;
COMMIT;
```

`COMMIT` saves everything since `BEGIN`. `ROLLBACK` throws it all away instead, as if none of it had happened.

Until you `COMMIT`, other connections to the database do not see your changes. In Python, `sqlite3` starts a transaction for you before an `INSERT`, `UPDATE`, or `DELETE`, which is why your Flask code must call `db.commit()` or the change is lost when the request ends.

Run `examples.sql`. It makes a change inside a transaction, rolls it back, and shows that nothing changed.
