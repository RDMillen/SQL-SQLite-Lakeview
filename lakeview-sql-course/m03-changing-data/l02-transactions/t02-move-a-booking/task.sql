-- Move booking 4 to room 201 and update its price, inside one transaction.
--
-- Tables you need:
--   bookings: id, user_id (links to users.id), room_id (links to rooms.id), check_in, check_out, occupants, total_price
--   rooms: id, number, room_type, capacity, price_per_night, available

BEGIN;
UPDATE bookings SET room_id = 4 WHERE id = 4;
UPDATE bookings SET total_price = 540.0 WHERE id = 4;
COMMIT;
