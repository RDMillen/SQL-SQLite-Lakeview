This course is for practising SQL with SQLite. It uses a small database for the Lakeview Hotel, on the shore of Toluca Lake. The same database is used in every task, so you get to know the data well.

## How the tasks work

Most tasks give you a file called `task.sql`. You write your SQL in that file and press Check. Hidden tests then run your SQL against a fresh copy of the database and compare what it does with what it should do. If something is wrong, the message tells you what to look at.

Each task folder also has two locked files:

- `lakeview.sql` builds the database. Open it to see every table and every row.
- `run.py` runs your SQL and prints the results. Right-click it and choose Run, or open it and press the green arrow.

Run your SQL before you press Check. Seeing the rows is the fastest way to spot a mistake.

The tests run your SQL a second time with some extra rows added to the database. This stops an answer that types out the expected rows by hand from passing. Write SQL that would still work if the data changed.

## Browsing the database (optional)

You do not need anything beyond `run.py` for this course. If you would like to click through the tables as well, every run of `run.py` saves a copy of the result as `practice.db` in the task folder. You can open it with:

- the Database tool window in the paid version of PyCharm: press +, then Data Source, then SQLite, and choose `practice.db`
- DB Browser for SQLite, a free program from sqlitebrowser.org

If `run.py` says that `practice.db` is in use, close it in the other program and run again.

## The Lakeview tables

| Table | What it holds |
|---|---|
| `users` | Guests who have an account |
| `rooms` | The five hotel rooms, with type, capacity, and nightly price |
| `bookings` | Who booked which room, the dates, the number of guests, and the total price |
| `extras` | Things a guest can add to a stay, such as breakfast |
| `booking_extras` | Which extras were added to which booking, and how many |

The file `examples.sql` in this task has a first query in it. Run `run.py` now to see the output, then move on.
