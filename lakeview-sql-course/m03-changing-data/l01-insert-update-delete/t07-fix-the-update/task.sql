-- This should save Eileen's phone number. Fix it so that only Eileen changes.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone

UPDATE users SET phone = '07700 900006' WHERE email = 'eileen@example.com';
