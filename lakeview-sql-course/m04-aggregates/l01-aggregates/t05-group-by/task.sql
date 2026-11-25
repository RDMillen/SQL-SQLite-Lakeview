-- Show each room_type and how many rooms there are of that type.
-- Name the count rooms. Sort by room_type.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT room_type, COUNT(*) AS rooms FROM rooms GROUP BY room_type ORDER BY room_type;
