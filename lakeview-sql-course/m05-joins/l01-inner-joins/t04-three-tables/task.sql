-- Show name, room number, check_in, check_out, and total_price for every booking.
-- Sort by check_in, then room number.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   users: id, name, email, password_hash, phone
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT u.name, r.number, b.check_in, b.check_out, b.total_price
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN rooms r ON b.room_id = r.id
ORDER BY b.check_in, r.number;
