# from crypt import methods
from crypt import methods
from flask_app.controllers import paintings
from flask_app import app
from flask_app.models import artist
from flask import Flask, render_template, request, session, flash, redirect
from flask_app.models.painting import Painting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/new/painting')
def new_painting():
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    #if in session, proceed to display page
    return render_template('create_painting.html', user=artist.User.get_one(data))

@app.route('/create/painting', methods=['POST'])
def create_painting():
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #validate user inputs
    if not Painting.validate_painting(request.form):
        return redirect('/new/painting')
    #declare the data we received
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "price": int(request.form['price']),
        "user_id": session['user_id']
    }
    Painting.save(data)
    return redirect('/dashboard')



@app.route('/edit/painting/<string:title>')
def edit(title):
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data
    data = {
        "title": title
    }
    session_data = {
        "id":session['user_id']
    }
    return render_template('edit_painting.html', painting=Painting.get_one_by_title(data), current_user=artist.User.get_one(session_data))


@app.route('/update/painting/<string:title>', methods=['POST'])
def update_painting(title):
    if 'user_id' not in session:
        return redirect('/logout')
    #validate user inputs
    if not Painting.validate_painting(request.form):
        return redirect('/new/painting')
    #declare needed data
    data = {
        "title":title,
        # "id": request.form['id'],
        "title": request.form['title'],
        "description": request.form['description'],
        "price": int(request.form['price'])
        # "user_id": session['user_id']
    }
    #invoke method save updates
    Painting.update_by_title(data)
    return redirect('/dashboard')

@app.route('/painting/<string:title>')
def show_painting(title):
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data
    data = {
        "title": title
    }
    session_data = {
        "id":session['user_id']
    }
    #invoke method to grab painting with specified id
    painting = Painting.get_one_by_title(data)
    return render_template('show_painting.html', painting = painting, current_user = artist.User.get_one(session_data))

@app.route('/destroy/painting/<string:title>')
def dunzo(title):
    #user must be in session bc anyone could delete paintings without logging in otherwise
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data we need to delete record
    data = {
        "title": title
    }
    #invoke delete method
    Painting.dunzo_by_title(data)
    #return to dash
    return redirect('/dashboard')
