Complete `register`. It inserts a user with the given `name` and `email` and the `password_hash` `demo-hash`, then commits.

`email` is `UNIQUE`, so registering an email twice raises `sqlite3.IntegrityError`. Catch it and return a message instead. Return these messages exactly, including the full stop:

- success: `Account created.`
- email already used: `That email address is already registered.`

## Tables you need

- `users`: `id`, `name`, `email`, `password_hash`, `phone`

Open `lakeview.sql` to see every row.
