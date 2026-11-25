-- Create the packages table described in the task.

CREATE TABLE packages (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price REAL NOT NULL CHECK (price >= 0),
    nights INTEGER NOT NULL DEFAULT 1 CHECK (nights > 0)
);
