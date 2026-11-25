SELECT date('2026-11-01', '+3 days') AS three_days_later;

SELECT id, check_in, check_out,
       CAST(julianday(check_out) - julianday(check_in) AS INTEGER) AS nights
FROM bookings;
