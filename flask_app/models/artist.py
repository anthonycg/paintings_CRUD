# from flask_bcrypt import Bcrypt
from flask import flash
import re
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    datbase_name = 'belt_exam'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO artists (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(), NOW())"
        results = connectToMySQL(cls.datbase_name).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM artists;"
        results = connectToMySQL(cls.datbase_name).query_db(query)
        artists = []
        for artist in results:
            artists.append(cls(artist))
        return artists

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM artists WHERE id = %(id)s;"
        results = connectToMySQL(cls.datbase_name).query_db(query, data)
        return cls(results[0])


    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM artists WHERE email = %(email)s;"
        results = connectToMySQL(cls.datbase_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(form):
        is_valid = True
        query = "SELECT * FROM artists WHERE email = %(email)s;"
        results = connectToMySQL('belt_exam').query_db(query, form)
        if len(results) >= 1:
            flash("Email is taken by another artist.")
            is_valid = False
        if len(form['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid Email address!")
            is_valid = False
        if form['confirm_password'] != form['password']:
            flash("Passwords do not match!")
        if len(form['password']) < 6:
            flash("Password Must be at least 8 characters.")
            is_valid = False
        return is_valid
