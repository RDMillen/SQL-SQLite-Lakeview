-- This query should show the number and room_type of every room that can be booked.
-- It has two mistakes. Fix them.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT number, room_type FROM rooms WHERE available = 1;
