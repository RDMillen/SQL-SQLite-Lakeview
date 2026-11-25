-- Add both new extras in one INSERT statement.
--
-- Tables you need:
--   extras: id, name, price

INSERT INTO extras (name, price) VALUES
    ('Dinner', 30.0),
    ('Spa pass', 22.5);
