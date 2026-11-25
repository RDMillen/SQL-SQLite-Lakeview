-- Lakeview Hotel drill database
-- This file builds the database used in every task. It is locked so that
-- everyone works with the same data. Read it to see the tables and rows.
--
-- The real Lakeview booking site stores Werkzeug password hashes. These
-- rows use 'demo-hash' because the drills never log anyone in.

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    number INTEGER NOT NULL UNIQUE,
    room_type TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    price_per_night REAL NOT NULL CHECK (price_per_night > 0),
    available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    check_in TEXT NOT NULL,
    check_out TEXT NOT NULL,
    occupants INTEGER NOT NULL CHECK (occupants > 0),
    total_price REAL NOT NULL
);

CREATE TABLE extras (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE booking_extras (
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    extra_id INTEGER NOT NULL REFERENCES extras(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (booking_id, extra_id)
);

INSERT INTO users (id, name, email, password_hash, phone) VALUES
    (1, 'James Sunderland', 'james@example.com', 'demo-hash', '07700 900001'),
    (2, 'Mary Sunderland', 'mary@example.com', 'demo-hash', '07700 900002'),
    (3, 'Harry Mason', 'harry@example.com', 'demo-hash', NULL),
    (4, 'Heather Mason', 'heather@example.com', 'demo-hash', '07700 900004'),
    (5, 'Henry Townshend', 'henry@example.com', 'demo-hash', NULL),
    (6, 'Eileen Galvin', 'eileen@example.com', 'demo-hash', NULL);

INSERT INTO rooms (id, number, room_type, capacity, price_per_night, available) VALUES
    (1, 101, 'Single', 1, 80.0, 1),
    (2, 102, 'Double', 2, 120.0, 0),
    (3, 103, 'Double', 2, 110.0, 1),
    (4, 201, 'Family', 4, 180.0, 1),
    (5, 312, 'Suite', 3, 250.0, 1);

-- Price rule: the nightly rate covers 2 guests, and each guest above 2
-- adds 10 per night.
INSERT INTO bookings (id, user_id, room_id, check_in, check_out, occupants, total_price) VALUES
    (1, 1, 1, '2026-11-01', '2026-11-04', 1, 240.0),
    (2, 2, 4, '2026-11-10', '2026-11-12', 3, 380.0),
    (3, 1, 1, '2026-12-01', '2026-12-03', 1, 160.0),
    (4, 3, 5, '2026-11-20', '2026-11-23', 2, 750.0),
    (5, 4, 3, '2026-11-04', '2026-11-06', 2, 220.0),
    (6, 5, 4, '2026-12-20', '2026-12-27', 4, 1400.0),
    (7, 2, 5, '2026-12-24', '2026-12-26', 3, 520.0),
    (8, 3, 3, '2026-12-01', '2026-12-02', 1, 110.0),
    (9, 4, 1, '2026-11-04', '2026-11-07', 1, 240.0),
    (10, 5, 5, '2027-01-02', '2027-01-05', 3, 780.0);

INSERT INTO extras (id, name, price) VALUES
    (1, 'Breakfast', 12.5),
    (2, 'Parking', 8.0),
    (3, 'Late checkout', 25.0),
    (4, 'Boat hire', 40.0);

INSERT INTO booking_extras (booking_id, extra_id, quantity) VALUES
    (1, 1, 3),
    (1, 2, 3),
    (2, 1, 6),
    (4, 1, 6),
    (4, 3, 1),
    (6, 1, 28),
    (6, 2, 7),
    (7, 3, 1),
    (9, 1, 3),
    (10, 2, 3);
