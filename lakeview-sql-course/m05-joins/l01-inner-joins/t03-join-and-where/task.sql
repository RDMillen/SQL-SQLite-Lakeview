-- Show booking id, room number, and room_type for bookings checking in during December 2026.
-- Sort by booking id.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT b.id, r.number, r.room_type
FROM bookings b
JOIN rooms r ON b.room_id = r.id
WHERE b.check_in BETWEEN '2026-12-01' AND '2026-12-31'
ORDER BY b.id;
