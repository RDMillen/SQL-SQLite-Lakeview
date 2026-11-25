-- This should create the cleaning_jobs table from the design in the task.
-- It has three mistakes.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

CREATE TABLE cleaning_jobs (
    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    job_date TEXT NOT NULL,
    minutes INTEGER NOT NULL CHECK (minutes > 0)
);
