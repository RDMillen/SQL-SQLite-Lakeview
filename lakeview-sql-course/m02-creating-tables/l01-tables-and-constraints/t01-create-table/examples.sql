CREATE TABLE guests (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    nights_stayed INTEGER NOT NULL DEFAULT 0 CHECK (nights_stayed >= 0)
);

INSERT INTO guests (name, email) VALUES ('Maria', 'maria@example.com');

SELECT * FROM guests;

-- This one is refused, because the email is already used.
INSERT INTO guests (name, email) VALUES ('Another Maria', 'maria@example.com');
