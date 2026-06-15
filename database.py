import sqlite3

conn = sqlite3.connect("movies.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    mood TEXT NOT NULL,
    actors TEXT NOT NULL,
    year INTEGER,
    rating REAL,
    description TEXT
)
""")

conn.commit()
conn.close()

print("База данных создана")