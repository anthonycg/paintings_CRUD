# from flask_bcrypt import Bcrypt
from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Painting:
    database_name = 'belt_exam'
    def __init__(self, data):
        self.id = data['id']
        self.id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO paintings (user_id, title, description, price, created_at, updated_at) VALUES (%(user_id)s, %(title)s,%(description)s,%(price)s, NOW(), NOW())"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results = connectToMySQL(cls.database_name).query_db(query)
        all_paintings = []
        for painting in results:
            all_paintings.append(cls(painting))
        return all_paintings

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_one_by_title(cls, data):
        query = "SELECT * FROM paintings WHERE title = %(title)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        print(results)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, updated_at=NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def update_by_title(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, updated_at=NOW() WHERE title = %(title)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def dunzo(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def dunzo_by_title(cls, data):
        query = "DELETE FROM paintings WHERE title = %(title)s"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @staticmethod
    def validate_painting(form):
        is_valid = True
        if len(form['title']) < 2:
            flash("Title must be at least 2 characters.")
            is_valid = False
        if len(form['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        if int(form['price']) < 10:
            flash("Price must be more than $10.")
            is_valid = False
        return is_valid