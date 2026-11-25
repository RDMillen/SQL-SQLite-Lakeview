-- Show the average price_per_night of available rooms, rounded to 2 decimal places.
-- Name the column average_price.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

SELECT ROUND(AVG(price_per_night), 2) AS average_price FROM rooms WHERE available = 1;
