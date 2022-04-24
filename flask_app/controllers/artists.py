from crypt import methods
# from msilib.schema import Patch
# from unittest.util import three_way_cmp
from flask_app import app
from flask_app.models import artist
from flask import Flask, render_template, request, session, flash, redirect
from flask_app.models.painting import Painting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    #validate user's inputs
    if not artist.User.validate_register(request.form):
        return redirect ('/')
    #create pw hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    #Grab data from webpage
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': request.form['confirm_password']
    }
    # Save the user's inputs into the DB -- INSERT INTO
    id = artist.User.save(data)
    #store user id into session
    session['user_id'] = id
    print(session['user_id'])
    print(id)
    return redirect ('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    #check if username exists in database
    current_user = artist.User.get_user_by_email(request.form)
    #if it doesn't, redirect to login page
    if not current_user:
        flash("Invalid Email/Password")
        return redirect('/')
    #if username does exist, check if it matches pw hash
    #if pw doesn't match:
    if not bcrypt.check_password_hash(current_user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    #if pw does match, redirect to dashboard -- user logged in:
    session['user_id'] = current_user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    #check if user_id is not in seesion
    if 'user_id' not in session:
        return redirect('/logout')
    # data = {
    #     "id": id
    # }
    session_data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user = artist.User.get_one(session_data), paintings = Painting.get_all_paintings_by_artist())

@app.route('/logout')
def logout():
    #clear session
    session.clear()
    return redirect('/')