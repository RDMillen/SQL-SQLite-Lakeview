A student's Flask app saves a booking for `user_id` 42. There is no user with id 42, and the `bookings` table has `REFERENCES users(id)`. SQLite gives no error and the booking is saved.

What is the most likely cause?
