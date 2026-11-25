-- Show each room_type and the total of total_price for its bookings.
-- Name the total takings. Highest first.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT r.room_type, SUM(b.total_price) AS takings
FROM bookings b
JOIN rooms r ON b.room_id = r.id
GROUP BY r.room_type
ORDER BY takings DESC;
