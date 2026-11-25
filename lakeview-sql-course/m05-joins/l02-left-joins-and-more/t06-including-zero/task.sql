-- Show every guest's name and number of bookings, including guests with 0.
-- Name the count bookings. Sort by name.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT u.name, COUNT(b.id) AS bookings
FROM users u
LEFT JOIN bookings b ON b.user_id = u.id
GROUP BY u.id
ORDER BY u.name;
