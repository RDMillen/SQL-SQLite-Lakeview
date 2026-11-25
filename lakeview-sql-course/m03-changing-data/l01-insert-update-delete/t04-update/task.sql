-- Make room 102 available again.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

UPDATE rooms SET available = 1 WHERE number = 102;
