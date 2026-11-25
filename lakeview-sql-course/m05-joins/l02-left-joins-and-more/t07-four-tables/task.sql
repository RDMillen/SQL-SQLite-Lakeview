-- Show guest name, check_in, extra (the extra's name), and quantity for every extra on a booking.
-- Sort by guest name, then check_in, then extra.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   booking_extras: booking_id (links to bookings.id), extra_id (links to extras.id), quantity
--   extras: id, name, price

SELECT u.name, b.check_in, e.name AS extra, be.quantity
FROM users u
JOIN bookings b ON b.user_id = u.id
JOIN booking_extras be ON be.booking_id = b.id
JOIN extras e ON be.extra_id = e.id
ORDER BY u.name, b.check_in, extra;
