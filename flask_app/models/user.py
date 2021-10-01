from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

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
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes').query_db( query, data )

    @staticmethod
    def validate_user(user):
        is_valid = True;
        if len(user['first_name']) < 3 or not user['first_name'].isalpha():
            flash("First Name must be at least 3 letters (A to Z)", "register")
            is_valid = False      
        if len(user['last_name']) < 3 or not user['last_name'].isalpha():
            flash("Last Name must be at least 3 letters (A to Z)", "register")
            is_valid = False      
        if not EMAIL_REGEX.match(user['email']): 
            flash("Email is not valid!", "register")
            is_valid = False   
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False       
        if not user['password'] == user['confirm']:
            flash("Passwords do not match!", "register")
            is_valid = False    
        users = User.get_all()
        for u in users:
            if user['email'] == u.email:
                flash("Email already assigned to another account", "register")
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True;
        if not EMAIL_REGEX.match(user['email']): 
            flash("Email is not valid!", "login")
            is_valid = False 
        return is_valid