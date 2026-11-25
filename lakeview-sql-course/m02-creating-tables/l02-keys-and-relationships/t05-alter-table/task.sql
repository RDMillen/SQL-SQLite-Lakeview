-- 1. Add the floor column to rooms.
-- 2. Set the floor of every room from the first digit of its number.
--
-- Tables you need:
--   rooms: id, number, room_type, capacity, price_per_night, available

ALTER TABLE rooms ADD COLUMN floor INTEGER NOT NULL DEFAULT 1;

UPDATE rooms SET floor = number / 100;
