-- Raise the price of every Double room by 10 percent, rounded to 2 decimal places.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

UPDATE rooms SET price_per_night = ROUND(price_per_night * 1.1, 2) WHERE room_type = 'Double';
