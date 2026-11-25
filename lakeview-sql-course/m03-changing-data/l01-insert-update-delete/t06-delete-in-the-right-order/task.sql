-- Delete booking 10 and the booking_extras rows that belong to it.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   booking_extras: booking_id (links to bookings.id), extra_id (links to extras.id), quantity

DELETE FROM booking_extras WHERE booking_id = 10;

DELETE FROM bookings WHERE id = 10;
