-- For each user_id, show the number of bookings and the total spent.
-- Biggest spender first, then lower user_id first.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT user_id, COUNT(*) AS bookings, SUM(total_price) AS spent
FROM bookings
GROUP BY user_id
ORDER BY spent DESC, user_id;
