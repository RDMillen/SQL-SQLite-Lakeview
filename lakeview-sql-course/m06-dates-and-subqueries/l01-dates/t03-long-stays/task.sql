-- Show id, check_in, and check_out of bookings longer than 2 nights.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT id, check_in, check_out
FROM bookings
WHERE julianday(check_out) - julianday(check_in) > 2;
