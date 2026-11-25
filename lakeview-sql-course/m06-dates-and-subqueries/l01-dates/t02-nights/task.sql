-- Show each booking's id and its number of nights as a whole number.
-- Name the column nights. Sort by id.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT id, CAST(julianday(check_out) - julianday(check_in) AS INTEGER) AS nights
FROM bookings
ORDER BY id;
