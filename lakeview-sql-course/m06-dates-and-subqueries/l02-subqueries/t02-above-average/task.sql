-- Show number and price_per_night of rooms cheaper than the average room.
-- Use a subquery.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT number, price_per_night
FROM rooms
WHERE price_per_night < (SELECT AVG(price_per_night) FROM rooms);
