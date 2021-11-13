from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import movie
from flask_bcrypt import Bcrypt

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


class User:

    def __init__(self, data):

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.movies = []

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE users.id=%(id)s;"
        results = connectToMySQL(
            'movies').query_db(query, data)
        return (cls(results[0]))

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL('movies').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('movies').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('movies').query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", "register")
            is_valid = False
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(
            'movies').query_db(query, user)
        if len(results) >= 1:
            flash("Email already exists", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characters", "register")
        if not any(char.isdigit() for char in user["password"]):
            flash('Password must have at least one number', "register")
            is_valid = False
        if not any(char.isupper() for char in user["password"]):
            flash('Password must have at least one uppercase letter', "register")
            is_valid = False
        if not user["password"] == user["confirm_password"]:
            flash("Passwords do not match", "register")
            is_valid = False
        return is_valid

    @classmethod
    def get_user_with_movies(cls, data):
        query = "SELECT * FROM users LEFT JOIN movies ON movies.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL('movies').query_db(query, data)
        user = cls(results[0])
        # empty_watchlist = []
        # if len(user) < 0:
        #     return empty_watchlist
        # else:
        for row_from_db in results:

            movie_data = {
                "id": row_from_db["movies.id"],
                "title": row_from_db["title"],
                "director": row_from_db["director"],
                "year": row_from_db["year"],
                "runtime": row_from_db["runtime"],
                "score": row_from_db["score"],
                "created_at": row_from_db["movies.created_at"],
                "updated_at": row_from_db["movies.updated_at"]
            }

            user.movies.append(movie.Movie(movie_data))
        return user

    @classmethod
    def get_user_with_watchlist(cls, data):
        query = "SELECT * FROM users LEFT JOIN watchlist ON users.id = watchlist.user_id LEFT JOIN movies ON movies.id = watchlist.movie_id WHERE users.id = %(id)s"
        results = connectToMySQL('movies').query_db(query, data)
        user = cls(results[0])

        for row_from_db in results:

            movie_data = {
                "id": row_from_db["movies.id"],
                "title": row_from_db["title"],
                "director": row_from_db["director"],
                "year": row_from_db["year"],
                "runtime": row_from_db["runtime"],
                "score": row_from_db["score"],
                "created_at": row_from_db["movies.created_at"],
                "updated_at": row_from_db["movies.updated_at"],
            }

            user.movies.append(movie.Movie(movie_data))
        return user

    @classmethod
    def add_to_watchlist(cls, data):
        query = "INSERT INTO watchlist (user_id, movie_id) VALUES (%(user_id)s , %(movie_id)s);"
        return connectToMySQL('movies').query_db(query, data)

    @classmethod
    def remove_from_watchlist(cls, data):
        query = "DELETE FROM watchlist WHERE user_id=%(user_id)s AND movie_id=%(movie_id)s;"
        return connectToMySQL('movies').query_db(query, data)

    # @classmethod
    # def get_users_with_bands(cls):
    #     query = "SELECT * FROM users JOIN bands ON bands.user_id = users.id"
    #     return connectToMySQL('band_together').query_db(query)
