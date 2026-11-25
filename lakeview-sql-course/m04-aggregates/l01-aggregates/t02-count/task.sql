-- Count the guests in the users table. Name the column guests.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone

SELECT COUNT(*) AS guests FROM users;
