-- Create the features and room_features tables described in the task.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

CREATE TABLE features (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE room_features (
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    feature_id INTEGER NOT NULL REFERENCES features(id),
    PRIMARY KEY (room_id, feature_id)
);
