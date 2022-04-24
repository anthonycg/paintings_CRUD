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



@app.route('/edit/painting/<int:id>')
def edit(id):
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data
    data = {
        "id": id
    }
    session_data = {
        "id":session['user_id']
    }
    return render_template('edit_painting.html', painting=Painting.get_one(data), current_user=artist.User.get_one(session_data))


@app.route('/update/painting/<int:id>', methods=['POST'])
def update_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    #validate user inputs
    if not Painting.validate_painting(request.form):
        return redirect('/new/painting')
    #declare needed data
    data = {
        "id":id,
        # "id": request.form['id'],
        "title": request.form['title'],
        "description": request.form['description'],
        "price": int(request.form['price'])
        # "user_id": session['user_id']
    }
    #invoke method save updates
    Painting.update(data)
    return redirect('/dashboard')

@app.route('/painting/<int:id>')
def show_painting(id):
    #check if user is in session
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data
    data = {
        "id": id
    }
    session_data = {
        "id":session['user_id']
    }
    #invoke method to grab painting with specified id
    painting = Painting.get_one_paintings_by_artist(data)
    return render_template('show_painting.html', painting = painting, current_user = artist.User.get_one(session_data))

@app.route('/destroy/painting/<int:id>')
def dunzo(id):
    #user must be in session bc anyone could delete paintings without logging in otherwise
    if 'user_id' not in session:
        return redirect('/logout')
    #declare needed data we need to delete record
    data = {
        "id": id
    }
    #invoke delete method
    Painting.dunzo_by_title(data)
    #return to dash
    return redirect('/dashboard')
