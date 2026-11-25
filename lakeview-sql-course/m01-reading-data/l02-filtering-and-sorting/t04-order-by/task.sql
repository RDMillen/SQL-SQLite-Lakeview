-- Show number, room_type, and price_per_night of every room,
-- most expensive first.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT number, room_type, price_per_night FROM rooms ORDER BY price_per_night DESC;
