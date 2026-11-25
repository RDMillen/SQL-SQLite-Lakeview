SELECT b.id, u.name, r.number
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN rooms r ON b.room_id = r.id;

SELECT r.number, b.id
FROM rooms r
LEFT JOIN bookings b ON b.room_id = r.id;
