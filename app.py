from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def get_recommendations(genre, mood, actor):

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            title,
            genre,
            mood,
            actors,
            year,
            rating,
            description
        FROM movies
    """)

    movies = cursor.fetchall()
    conn.close()

    recommendations = []

    for movie in movies:

        score = 0

        movie_title = movie[0]
        movie_genre = movie[1]
        movie_mood = movie[2]
        movie_actor = movie[3]
        movie_year = movie[4]
        movie_rating = movie[5]
        movie_description = movie[6]

        if movie_genre == genre:
            score += 12

        if movie_mood == mood:
            score += 5

        if actor.lower() in movie_actor.lower():
            score += 8

        recommendations.append({
            "title": movie_title,
            "genre": movie_genre,
            "mood": movie_mood,
            "actors": movie_actor,
            "year": movie_year,
            "rating": movie_rating,
            "description": movie_description,
            "score": score
        })

    recommendations.sort(
        key=lambda x: (x["score"], x["rating"]),
        reverse=True
    )

    return recommendations[:5]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


@app.route('/result', methods=['POST'])
def result():

    genre = request.form.get('genre')
    mood = request.form.get('mood')
    actor = request.form.get('actor')

    movies = get_recommendations(
        genre,
        mood,
        actor
    )

    return render_template(
        'result.html',
        movies=movies,
        genre=genre,
        mood=mood,
        actor=actor
    )


if __name__ == '__main__':
    app.run(debug=True)