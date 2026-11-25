BEGIN;
DELETE FROM booking_extras;
SELECT COUNT(*) AS rows_inside_transaction FROM booking_extras;
ROLLBACK;

SELECT COUNT(*) AS rows_after_rollback FROM booking_extras;
