from flask import render_template
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
def home_page():
    friday_pick = 'Extraction 2'
    return render_template('index.jinja', chosen=friday_pick)

@app.route('/sign_in')
def sign_in():
    login_form = LoginForm()
    return render_template('sign_in.jinja', form=login_form)

@app.route('/register')
def register():
    register_form = RegisterForm()
    return render_template('register.jinja', form=register_form)

@app.route('/suggested')
def suggested():
    movie_list = ['Shaun of the Dead', 'Hot Fuzz', "The World's End", "A Ghost Story"]
    return render_template('suggested.jinja', movie_list=movie_list)

@app.route('/about')
def about():
    return render_template('about.jinja')