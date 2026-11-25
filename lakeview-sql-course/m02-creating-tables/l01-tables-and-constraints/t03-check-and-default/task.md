Lakeview sells packages such as a lakeside weekend. Write a `CREATE TABLE` statement for a table called `packages`:

| Column | Type | Rules |
|---|---|---|
| `id` | `INTEGER` | primary key |
| `name` | `TEXT` | must have a value, and must be unique |
| `price` | `REAL` | must have a value, and cannot be below 0 |
| `nights` | `INTEGER` | must have a value, must be more than 0, and is 1 if not given |

You need `CHECK` for the two number rules and `DEFAULT` for the last one.
