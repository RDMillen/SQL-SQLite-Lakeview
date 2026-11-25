-- Create the reviews table described in the task.
-- This task runs on the full Lakeview database.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone
--   rooms: id, number, room_type, capacity, price_per_night, available

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT
);
