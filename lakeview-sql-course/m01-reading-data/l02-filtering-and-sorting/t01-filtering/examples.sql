SELECT number, price_per_night FROM rooms WHERE price_per_night > 100;

SELECT number FROM rooms WHERE available = 1 AND (room_type = 'Double' OR room_type = 'Suite');

SELECT number, room_type, price_per_night FROM rooms ORDER BY room_type, price_per_night DESC;

SELECT DISTINCT room_type FROM rooms;

SELECT name, phone FROM users WHERE phone IS NULL;
