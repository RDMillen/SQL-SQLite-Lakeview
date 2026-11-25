SELECT COUNT(*) AS bookings, SUM(total_price) AS takings FROM bookings;

SELECT room_type, COUNT(*) AS rooms FROM rooms GROUP BY room_type;

SELECT user_id, COUNT(*) AS bookings
FROM bookings
WHERE check_in >= '2026-12-01'
GROUP BY user_id
HAVING COUNT(*) >= 1;
