from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


#adding regex
EMEAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#  model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    
    
    @classmethod
    def save(cls, data):
        #always have to pass in"cls" because it's a class method
        query = """
                INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
             """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('login_and_validation').query_db(query, data)
    

    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM users
                WHERE email = %(email)s;
                """
        result = connectToMySQL("login_and_validation").query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * FROM users
        WHERE id = %(id)s;"""
        result = connectToMySQL("login_and_validation").query_db(query, data)
        if result == False or len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("Must enter first name longer than two chracters")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Must enter first name longer than two chracters")
            is_valid = False
        if not EMEAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if user["password"] != user['confirm_password']:
            flash("Passwords do not match!")
            is_valid = False
        return is_valid