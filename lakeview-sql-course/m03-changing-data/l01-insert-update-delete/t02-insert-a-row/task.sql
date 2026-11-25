-- Add Maria to the users table.
--
-- Tables you need:
--   users: id, name, email, password_hash, phone

INSERT INTO users (name, email, password_hash) VALUES ('Maria', 'maria@example.com', 'demo-hash');
