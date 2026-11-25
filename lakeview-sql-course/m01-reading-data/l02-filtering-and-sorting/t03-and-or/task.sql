-- Show the number and room_type of rooms that are available
-- and have a capacity of at least 2.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT number, room_type FROM rooms WHERE available = 1 AND capacity >= 2;
