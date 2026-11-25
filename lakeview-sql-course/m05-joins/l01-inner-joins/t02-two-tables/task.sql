-- Show each booking's id, the guest's name, and check_in. Sort by booking id.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   users: id, name, email, password_hash, phone

SELECT b.id, u.name, b.check_in
FROM bookings b
JOIN users u ON b.user_id = u.id
ORDER BY b.id;
