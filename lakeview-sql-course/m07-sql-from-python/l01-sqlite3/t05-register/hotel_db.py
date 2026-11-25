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


def find_room(conn, number):
    """Return the number, room_type, and price_per_night of the room with this number, or None."""
    return conn.execute(
        "SELECT number, room_type, price_per_night FROM rooms WHERE number = ?",
        (number,),
    ).fetchone()


def add_extra(conn, name, price):
    """Add an extra, save the change, and return the new extra's id."""
    cursor = conn.execute("INSERT INTO extras (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    return cursor.lastrowid


def register(conn, name, email):
    """Add a user with password_hash 'demo-hash' and return a message for the user."""
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, 'demo-hash')",
            (name, email),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return "That email address is already registered."
    return "Account created."


if __name__ == "__main__":
    # Try your functions here. Right-click this file and choose Run.
    from pathlib import Path

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((Path(__file__).parent / "lakeview.sql").read_text(encoding="utf-8"))
    for room in get_rooms(conn):
        print(tuple(room))
    print(find_room(conn, 312) and tuple(find_room(conn, 312)))
    print(find_room(conn, 999))
    print(add_extra(conn, 'Dinner', 30.0))
    print(register(conn, 'Maria', 'maria@example.com'))
    print(register(conn, 'Maria', 'maria@example.com'))
