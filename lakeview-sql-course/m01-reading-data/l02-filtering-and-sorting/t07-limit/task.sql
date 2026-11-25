-- Show the number and price_per_night of the three cheapest rooms, cheapest first.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT number, price_per_night FROM rooms ORDER BY price_per_night LIMIT 3;
