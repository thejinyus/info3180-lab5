"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from models import UserProfile


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        firstname = form.firstname.data
        lastname = form.lastname.data
        gender = form.gender.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        
        user = UserProfile(
            first_name=firstname,
            last_name=lastname, 
            gender=gender,
            email=email,
            location = location,
            biography=biography)
            
        db.session.add(user)
        db.session.commit()
        
        #user = UserProfile.query.filter_by(username=username).first()
        
    return render_template('home.html',form=form)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/profiles/')
def profiles():
    return render_template("profiles.html")
    
@app.route('/profile/<userid>')
def profile(userid):
    
    user = UserProfile.query.filter_by(id=userid).first()
    
    firstname = user.first_name
    lastname = user.last_name
    gender = user.gender
    email = user.email
    location = user.location
    biography = user.biography
    
    
    
    
    return render_template("profile.html", 
    firstname = user.firstname,
    lastname = user.lastname,
    gender = user.gender,
    email = user.email,
    location = user.location,
    biography = user.biography)
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        firstname = form.firstname.data
        lastname = form.lastname.data
        gender = form.gender.data
        email = form.email.data
        location = form.location.data
        bio = form.biography.data
        
        user = UserProfile.query.filter_by(username=username).first()
        
        if user is not None and user.password == password:

            # using your model, query database for a user based on the username
            # and password submitted
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.

            # get user id, load into session
            login_user(user)

            # remember to flash a message to the user
            flash('Logged in successfully.', 'success')
            return redirect(url_for("secure_page"))  # they should be redirected to a secure-page route instead
        else:
            error = 'Invalid username or password'
            flash("Incorrect Username or Password", "danger")
    return render_template("login.html", form=form)
    
@app.route("/secure-page")
@login_required
def secure_page():
    return render_template("secure_page.html")

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out', 'success')
    return redirect(url_for('home'))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
