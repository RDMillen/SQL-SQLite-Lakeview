-- Add up total_price for every booking. Name the column takings.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT SUM(total_price) AS takings FROM bookings;
