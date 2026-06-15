import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

cursor.execute("SELECT title, genre, actors FROM movies")

for movie in cursor.fetchall():
    print(movie)

conn.close()