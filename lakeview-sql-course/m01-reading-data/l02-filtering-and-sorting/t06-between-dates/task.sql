-- Show id, check_in, and check_out of bookings that check in during November 2026.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT id, check_in, check_out FROM bookings WHERE check_in BETWEEN '2026-11-01' AND '2026-11-30';
