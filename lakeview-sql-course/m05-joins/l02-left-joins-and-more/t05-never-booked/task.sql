-- Show the number of every room that has never been booked. Use a LEFT JOIN.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price

SELECT r.number
FROM rooms r
LEFT JOIN bookings b ON b.room_id = r.id
WHERE b.id IS NULL;
