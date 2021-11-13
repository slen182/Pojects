from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user


class Movie:

    def __init__(self, data):

        self.id = data['id']
        self.title = data['title']
        self.director = data['director']
        self.year = data['year']
        self.runtime = data['runtime']
        self.score = data['score']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO movies ( title, director, year, runtime, score, user_id, created_at, updated_at ) VALUES ( %(title)s , %(director)s , %(year)s , %(runtime)s , %(score)s , %(user_id)s, NOW() , NOW() );"
        return connectToMySQL('movies').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM movies WHERE user_id=%(user_id)s AND movies.id=%(movie_id)s;"
        return connectToMySQL('movies').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM movies WHERE user_id=%(user_id)s AND movies.id=%(movie_id)s;"
        results = connectToMySQL(
            'movies').query_db(query, data)
        return (cls(results[0]))

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movies"
        return connectToMySQL('movies').query_db(query)

    @classmethod
    def get_all_complete(cls):
        query = "SELECT * FROM movies LEFT JOIN users ON movies.user_id = users.id;"
        results = connectToMySQL('movies').query_db(query)
        new_movies = []
        if len(results) == 0:
            return new_movies
        else:
            for movie in results:
                user_data = {
                    "id": movie["users.id"],
                    "first_name": movie["first_name"],
                    "last_name": movie["last_name"],
                    "email": movie["email"],
                    "password": movie["password"],
                    "created_at": movie["users.created_at"],
                    "updated_at": movie["users.updated_at"]
                }
                creator = user.User(user_data)
                new_movie = cls(movie)
                new_movie.creator = creator
                new_movies.append(new_movie)
            return new_movies

    @classmethod
    def get_all_complete_title(cls):
        query = "SELECT * FROM movies LEFT JOIN users ON movies.user_id = users.id ORDER BY title ASC;"
        results = connectToMySQL('movies').query_db(query)
        new_movies = []
        if len(results) == 0:
            return new_movies
        else:
            for movie in results:
                user_data = {
                    "id": movie["users.id"],
                    "first_name": movie["first_name"],
                    "last_name": movie["last_name"],
                    "email": movie["email"],
                    "password": movie["password"],
                    "created_at": movie["users.created_at"],
                    "updated_at": movie["users.updated_at"]
                }
                creator = user.User(user_data)
                new_movie = cls(movie)
                new_movie.creator = creator
                new_movies.append(new_movie)
            return new_movies

    @classmethod
    def get_all_complete_director(cls):
        query = "SELECT * FROM movies LEFT JOIN users ON movies.user_id = users.id ORDER BY director ASC;"
        results = connectToMySQL('movies').query_db(query)
        new_movies = []
        if len(results) == 0:
            return new_movies
        else:
            for movie in results:
                user_data = {
                    "id": movie["users.id"],
                    "first_name": movie["first_name"],
                    "last_name": movie["last_name"],
                    "email": movie["email"],
                    "password": movie["password"],
                    "created_at": movie["users.created_at"],
                    "updated_at": movie["users.updated_at"]
                }
                creator = user.User(user_data)
                new_movie = cls(movie)
                new_movie.creator = creator
                new_movies.append(new_movie)
            return new_movies

    @classmethod
    def get_all_complete_year(cls):
        query = "SELECT * FROM movies LEFT JOIN users ON movies.user_id = users.id ORDER BY year ASC;"
        results = connectToMySQL('movies').query_db(query)
        new_movies = []
        if len(results) == 0:
            return new_movies
        else:
            for movie in results:
                user_data = {
                    "id": movie["users.id"],
                    "first_name": movie["first_name"],
                    "last_name": movie["last_name"],
                    "email": movie["email"],
                    "password": movie["password"],
                    "created_at": movie["users.created_at"],
                    "updated_at": movie["users.updated_at"]
                }
                creator = user.User(user_data)
                new_movie = cls(movie)
                new_movie.creator = creator
                new_movies.append(new_movie)
            return new_movies

    @classmethod
    def get_all_complete_runtime(cls):
        query = "SELECT * FROM movies LEFT JOIN users ON movies.user_id = users.id ORDER BY runtime ASC;"
        results = connectToMySQL('movies').query_db(query)
        new_movies = []
        if len(results) == 0:
            return new_movies
        else:
            for movie in results:
                user_data = {
                    "id": movie["users.id"],
                    "first_name": movie["first_name"],
                    "last_name": movie["last_name"],
                    "email": movie["email"],
                    "password": movie["password"],
                    "created_at": movie["users.created_at"],
                    "updated_at": movie["users.updated_at"]
                }
                creator = user.User(user_data)
                new_movie = cls(movie)
                new_movie.creator = creator
                new_movies.append(new_movie)
            return new_movies

    @classmethod
    def get_all_complete_score(cls):
        query = "SELECT * FROM movies LEFT JOIN users ON movies.user_id = users.id ORDER BY score DESC;"
        results = connectToMySQL('movies').query_db(query)
        new_movies = []
        if len(results) == 0:
            return new_movies
        else:
            for movie in results:
                user_data = {
                    "id": movie["users.id"],
                    "first_name": movie["first_name"],
                    "last_name": movie["last_name"],
                    "email": movie["email"],
                    "password": movie["password"],
                    "created_at": movie["users.created_at"],
                    "updated_at": movie["users.updated_at"]
                }
                creator = user.User(user_data)
                new_movie = cls(movie)
                new_movie.creator = creator
                new_movies.append(new_movie)
            return new_movies

    @classmethod
    def update(cls, data):
        query = "UPDATE movies SET title=%(title)s, director=%(director)s, year = %(year)s, runtime = %(runtime)s, score = %(score)s, user_id=%(user_id)s, updated_at = NOW() WHERE user_id=%(user_id)s AND movies.id=%(movie_id)s;"
        return connectToMySQL('movies').query_db(query, data)

    @staticmethod
    def validate_movie(movie):
        is_valid = True
        if len(movie['title']) < 2:
            flash("Title must be at least 2 characters", "movie")
            is_valid = False
        if len(movie['director']) < 2:
            flash("Director name must be at least 2 characters", "movie")
            is_valid = False
        if len(movie['year']) > 4:
            flash("Please enter a valid year", "movie")
            is_valid = False
        if len(movie['year']) < 4:
            flash("Please enter a valid year", "movie")
            is_valid = False
        if len(movie['runtime']) < 1:
            flash("Runtime must be at least 1 character", "movie")
            is_valid = False
        if len(movie['score']) < 1:
            flash("Score must be at least 1 characters", "movie")
            is_valid = False
        if len(movie['score']) > 3:
            flash("Score can be no more than 3 characters", "movie")
            is_valid = False
        return is_valid
