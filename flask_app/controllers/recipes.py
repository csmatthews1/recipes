from flask_app import app
from flask import Flask,render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash

@app.route('/create')         
def create_recipe():
    return render_template("create.html")

@app.route('/addrecipe', methods=['POST'])         
def add_recipe():
    if not Recipe.validate(request.form):
        return redirect('/create')

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': request.form['under30'],
        'author_id': session['user'],
        'created_at': request.form['created_at']
    }
    Recipe.save(data)
    return redirect("/recipes")

@app.route('/view/<int:id>')         
def view_recipe(id):
    data = {
        'id': id
    }
    recipe = Recipe.get_by_id(data)

    return render_template("view.html", recipe = recipe)

@app.route('/edit/<int:id>')         
def edit_recipe(id):
    data = {
        'id': id
    }
    recipe = Recipe.get_by_id(data)
    return render_template("edit.html", recipe = recipe)

@app.route('/editrecipe', methods=['POST'])         
def update():
    if not Recipe.validate(request.form):
        return redirect('/edit/'+request.form['id'])
        
    data = {
        'id'  : request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': request.form['under30'],
        'author_id': session['user'],
        'created_at': request.form['created_at']
    }
    Recipe.update(data)
    return redirect("/recipes")

@app.route('/delete/<int:id>')         
def delete_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect("/recipes")
