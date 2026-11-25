-- Show id, check_in, and check_out of bookings for room 101 that clash with
-- a new stay from 2026-11-03 to 2026-11-05.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT id, check_in, check_out
FROM bookings
WHERE room_id = 1
  AND check_in < '2026-11-05'
  AND check_out > '2026-11-03';
