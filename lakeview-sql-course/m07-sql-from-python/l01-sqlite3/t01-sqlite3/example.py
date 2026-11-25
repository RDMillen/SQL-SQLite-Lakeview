import sqlite3
from pathlib import Path

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript((Path(__file__).parent / "lakeview.sql").read_text(encoding="utf-8"))

for row in conn.execute("SELECT number, price_per_night FROM rooms").fetchall():
    print(row["number"], row["price_per_night"])

email = "mary@example.com"
user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
print(dict(user))

try:
    conn.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                 ("Mary again", email, "demo-hash"))
except sqlite3.IntegrityError as error:
    print("Refused:", error)
