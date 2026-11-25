-- Show the user_id and number of bookings of guests with more than one booking.
-- Name the count bookings. Sort by user_id.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT user_id, COUNT(*) AS bookings
FROM bookings
GROUP BY user_id
HAVING COUNT(*) > 1
ORDER BY user_id;
