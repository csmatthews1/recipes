from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.author_id = data['author_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes').query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes ( name, description, instructions, under30, author_id, created_at, updated_at) VALUES ( %(name)s, %(description)s, %(instructions)s, %(under30)s, %(author_id)s, %(created_at)s, NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, created_at = %(created_at)s, updated_at = NOW() WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        print(query)
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes').query_db( query, data )
    
    @staticmethod
    def validate(recipe):
        is_valid = True;
        if len(recipe['name']) < 3:
            flash("Recipe Name must be at least 3 characters")
            is_valid = False      
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False      
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters")
            is_valid = False       
        if not recipe['created_at']:
            flash("Date created is required", "register")
            is_valid = False    
        return is_valid
