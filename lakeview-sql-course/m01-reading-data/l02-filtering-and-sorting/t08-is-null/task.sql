-- Show the name and email of guests with no phone number.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone

SELECT name, email FROM users WHERE phone IS NULL;
