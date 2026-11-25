-- Show the number and price_per_night of rooms that cost less than 150 a night.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT number, price_per_night FROM rooms WHERE price_per_night < 150;
