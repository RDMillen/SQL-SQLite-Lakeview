-- Show the number of every available room with no clashing booking
-- for a stay from 2026-12-01 to 2026-12-03. Sort by number.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT r.number
FROM rooms r
WHERE r.available = 1
  AND NOT EXISTS (
      SELECT 1 FROM bookings b
      WHERE b.room_id = r.id
        AND b.check_in < '2026-12-03'
        AND b.check_out > '2026-12-01'
  )
ORDER BY r.number;
