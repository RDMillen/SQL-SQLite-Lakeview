-- Show the name of every guest with a booking for room number 312.
-- Each guest once. Sort by name.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT name FROM users
WHERE id IN (
    SELECT user_id FROM bookings
    WHERE room_id = (SELECT id FROM rooms WHERE number = 312)
)
ORDER BY name;
