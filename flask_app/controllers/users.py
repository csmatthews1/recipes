from flask_app import app
from flask import Flask,render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

@app.route('/')         
def index():
    return render_template("index.html")
    
@app.route('/register', methods=['POST'])         
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user = User.save(data)
    session['user'] = user
    return redirect("/recipes")
    
@app.route('/login', methods=['POST'])         
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect ('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect ('/')

    session['user'] = user_in_db.id
    return redirect("/recipes")
    
@app.route('/recipes')         
def result():
    data = {
        'id': session['user']
    }
    user = User.get_by_id(data)
    recipes = Recipe.get_all()
    return render_template('recipes.html', user = user, recipes = recipes)
    
@app.route('/logout')         
def logout():
    session.clear()
    return redirect('/')
