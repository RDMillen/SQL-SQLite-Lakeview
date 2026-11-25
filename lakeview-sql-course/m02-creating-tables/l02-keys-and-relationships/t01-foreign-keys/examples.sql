-- Guest 99 does not exist, so this is refused.
INSERT INTO bookings (user_id, room_id, check_in, check_out, occupants, total_price)
VALUES (99, 1, '2027-02-01', '2027-02-02', 1, 80.0);
