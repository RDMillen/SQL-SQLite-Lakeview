A foreign key is a column that points at the primary key of another table. In Lakeview, `bookings.user_id` points at `users.id`, so every booking belongs to a real guest.

```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    ...
);
```

`REFERENCES users(id)` is the foreign key. With it in place, SQLite refuses a booking for a guest who does not exist, and refuses to delete a guest who still has bookings.

## Turn foreign keys on

SQLite only checks foreign keys when you ask it to, once for each connection:

```sql
PRAGMA foreign_keys = ON;
```

`run.py` and the tests in this course always turn it on. In your own Flask project, `get_db()` should run this straight after connecting. If you forget, SQLite stores bookings for guests who do not exist and gives no error. This catches a lot of people out.

## ON DELETE

You can say what happens to the child rows when the parent row is deleted:

| Option | When a guest is deleted |
|---|---|
| (none given) | refused while the guest has bookings |
| `ON DELETE CASCADE` | their bookings are deleted too |
| `ON DELETE SET NULL` | their bookings stay, with `user_id` set to `NULL` |

## Many-to-many relationships

One booking can have many extras, and one extra can be on many bookings. A table in the middle, often called a junction or link table, holds one row for each pairing. In Lakeview this is `booking_extras`:

```sql
CREATE TABLE booking_extras (
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    extra_id INTEGER NOT NULL REFERENCES extras(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (booking_id, extra_id)
);
```

The primary key is made of both columns together, so the same extra cannot be added to the same booking twice. This is called a composite key.

The tasks in this lesson run on the full Lakeview database, so your new tables can point at `users`, `rooms`, and the rest. Run `examples.sql` to see a foreign key refuse a row.
