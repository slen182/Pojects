from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def reroute():
    return redirect('/users')


@app.route("/users")
def index():
    return render_template("index.html")


@app.route('/users/register', methods=["POST"])
def create_user():
    if not User.validate_registration(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id

    return redirect('/users/dashboard/')


@app.route('/users/login', methods=["POST"])
def login_user():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/users/dashboard/')


@app.route('/users/dashboard/')
def display_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }

    user = User.get_by_id(user_data)
    movies = Movie.get_all_complete()

    return render_template("dashboard.html", user=user, movies=movies)


@app.route('/users/dashboard/title')
def display_dashboard_by_title():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }

    user = User.get_by_id(user_data)
    movies = Movie.get_all_complete_title()

    return render_template("dashboard.html", user=user, movies=movies)


@app.route('/users/dashboard/director')
def display_dashboard_by_director():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }

    user = User.get_by_id(user_data)

    movies = Movie.get_all_complete_director()

    return render_template("dashboard.html", user=user, movies=movies)


@app.route('/users/dashboard/year')
def display_dashboard_by_year():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }

    user = User.get_by_id(user_data)

    movies = Movie.get_all_complete_year()

    return render_template("dashboard.html", user=user, movies=movies)


@app.route('/users/dashboard/runtime')
def display_dashboard_by_runtime():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }

    user = User.get_by_id(user_data)

    movies = Movie.get_all_complete_runtime()

    return render_template("dashboard.html", user=user, movies=movies)


@app.route('/users/dashboard/score')
def display_dashboard_by_score():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }

    user = User.get_by_id(user_data)

    movies = Movie.get_all_complete_score()

    return render_template("dashboard.html", user=user, movies=movies)


@ app.route('/users/logout')
def logout_user():
    session.clear()
    return redirect('/')


@ app.route('/users/create')
def create_movie():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    return render_template("new.html", user=user)


@ app.route('/users/add', methods=['POST'])
def add_movie():
    if 'user_id' not in session:
        return redirect('/')
    if not Movie.validate_movie(request.form):
        return redirect('/users/create')
    data = {
        "title": request.form["title"],
        "director": request.form["director"],
        "year": request.form["year"],
        "runtime": request.form["runtime"],
        "score": request.form["score"],
        "user_id": session["user_id"]
    }
    Movie.save(data)

    return redirect('/users/dashboard')


@app.route('/users/edit/<int:movie_id>')
def edit_movie(movie_id):
    if 'user_id' not in session:
        return redirect('/')
    movie_data = {
        'user_id': session['user_id'],
        'movie_id': movie_id
    }

    movie = Movie.get_one(movie_data)
    return render_template("edit.html", movie=movie)


@app.route('/users/update/<int:movie_id>', methods=['POST'])
def update_movie(movie_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Movie.validate_movie(request.form):
        return redirect(f'/users/edit/{movie_id}')
    data = {
        "title": request.form["title"],
        "director": request.form["director"],
        "year": request.form["year"],
        "runtime": request.form["runtime"],
        "score": request.form["score"],
        "user_id": session['user_id'],
        "movie_id": movie_id
    }
    Movie.update(data)
    return redirect('/users/dashboard')


@app.route('/users/display')
def view_movies():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_user_with_movies(data)
    return render_template("view.html", user=user)


@app.route('/users/<int:movie_id>/delete')
def delete_movie(movie_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'movie_id': movie_id
    }
    Movie.delete(data)
    return redirect("/users/dashboard")


@app.route('/users/<int:movie_id>/delete_from_view')
def delete_movie_from_view(movie_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'movie_id': movie_id
    }
    Movie.delete(data)
    return redirect("/users/display")


@app.route('/users/watchlist')
def view_watchlist():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_user_with_watchlist(data)
    return render_template("watchlist.html", user=user)


@app.route('/users/watchlist/add/<int:movie_id>')
def add_to_watchlist(movie_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"],
        "movie_id": movie_id
    }

    User.add_to_watchlist(data)
    return redirect('/users/watchlist')


@app.route('/users/watchlist/remove/<int:movie_id>')
def remove_from_watchlist(movie_id):
    data = {
        'user_id': session['user_id'],
        'movie_id': movie_id
    }

    User.remove_from_watchlist(data)

    return redirect('/users/watchlist')
