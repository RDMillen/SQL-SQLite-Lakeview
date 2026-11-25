"""Lakeview database functions.

Every function takes an open sqlite3 connection as its first argument.
The tests pass in a connection to a fresh copy of the Lakeview database
with row_factory set to sqlite3.Row.
"""

import sqlite3


def get_rooms(conn):
    """Return the number, room_type, and price_per_night of every room, sorted by number."""
    return conn.execute(
        "SELECT number, room_type, price_per_night FROM rooms ORDER BY number"
    ).fetchall()


if __name__ == "__main__":
    # Try your functions here. Right-click this file and choose Run.
    from pathlib import Path

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((Path(__file__).parent / "lakeview.sql").read_text(encoding="utf-8"))
    for room in get_rooms(conn):
        print(tuple(room))
