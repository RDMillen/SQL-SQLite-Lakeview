SELECT number, price_per_night
FROM rooms
WHERE price_per_night > (SELECT AVG(price_per_night) FROM rooms);

SELECT r.number
FROM rooms r
WHERE NOT EXISTS (
    SELECT 1 FROM bookings b
    WHERE b.room_id = r.id
      AND b.check_in BETWEEN '2026-12-01' AND '2026-12-31'
);
