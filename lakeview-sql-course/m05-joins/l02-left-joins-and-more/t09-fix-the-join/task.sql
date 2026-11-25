-- This should show each booking's id, the guest's name, and the room number.
-- Run it, read the error, then fix it.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   users: id, name, email, password_hash, phone
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT bookings.id, name, number
FROM bookings
JOIN users ON user_id = users.id
JOIN rooms ON room_id = rooms.id
ORDER BY bookings.id;
