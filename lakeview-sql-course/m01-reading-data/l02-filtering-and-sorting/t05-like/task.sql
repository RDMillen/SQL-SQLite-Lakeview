-- Show the name and email of every guest whose surname is Mason.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone

SELECT name, email FROM users WHERE name LIKE '% Mason';
