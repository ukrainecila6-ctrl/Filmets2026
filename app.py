from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "filmec_secret_key"


reviews_list = [
    {
        "name": "Иван",
        "text": "Очень удобный сервис для подбора фильмов."
    },
    {
        "name": "Анна",
        "text": "Нашла несколько отличных фильмов на вечер."
    }
]


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

    username = session.get('username')

    return render_template(
        'index.html',
        username=username
    )


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()

            session['username'] = username

            return redirect('/')

        except sqlite3.IntegrityError:
            flash("Пользователь уже существует")

        finally:
            conn.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['username'] = username

            return redirect('/')

        flash("Неверный логин или пароль")

    return render_template('login.html')


@app.route('/logout')
def logout():

    session.pop('username', None)

    return redirect('/')


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


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'POST':

        name = request.form.get('name')
        text = request.form.get('text')

        if name and text:

            reviews_list.append({
                "name": name,
                "text": text
            })

        return redirect('/reviews')

    return render_template(
        'reviews.html',
        reviews=reviews_list
    )


if __name__ == '__main__':
    app.run(debug=True)