from flask import render_template, redirect, flash
from app import app
from app.forms import LoginForm, RegisterForm, AddMovieForm, VoteForm
from app.models import User, Movie

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    friday_pick = ''
    mf = AddMovieForm()
    if mf.validate_on_submit():
        movies = Movie.query.filter_by(title=mf.title.data).first()
        if movies and movies.if_recommended(mf.year.data):
            flash(f'{mf.title.data} has already been recommended!')
        else:
            movie = Movie(title = mf.title.data,
                          user_id = 1,
                          release_year = str(mf.year.data),
                          description = mf.description.data,
                          )
            movie.commit()
            flash(f'{mf.title.data} has been added to the list!')
            return redirect('/')
    return render_template('index.jinja', chosen=friday_pick, form=mf)

@app.route('/sign_in', methods = ['GET', 'POST'])
def sign_in():
    lf = LoginForm()
    if lf.validate_on_submit():
        users = User.query.filter_by(email=lf.email.data).first()
        if users and users.check_password(lf.password.data):
            flash(f'{lf.email.data} logged in!')
            return redirect('/')
        else:
            flash(f'Invalid User Data, Try Again')
    return render_template('sign_in.jinja', form=lf)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    rf = RegisterForm()
    if rf.validate_on_submit():
        user_filter = User.query.filter_by(username=rf.username.data).first()
        email_filter = User.query.filter_by(email=rf.email.data).first()
        if user_filter or email_filter:
            flash(f'Username or Email already taken. Please Sign in <a href="/sign_in">here</a>.')
        else:
            user = User(fname=rf.fname.data, 
                        lname=rf.lname.data, 
                        username=rf.username.data, 
                        email=rf.email.data)
            user.hash_password(rf.password.data)
            user.commit()
            print(user)
            flash(f'{rf.fname.data if rf.fname.data else rf.username.data} registered')
            return redirect('/')
    return render_template('register.jinja', form=rf)

@app.route('/suggested')
def suggested():
    vf = VoteForm()
    movie_list = Movie.query.all()
    return render_template('suggested.jinja', movie_list=movie_list, form=vf)

@app.route('/about')
def about():
    return render_template('about.jinja')