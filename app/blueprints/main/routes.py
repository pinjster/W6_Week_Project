from flask import g, render_template, flash, redirect, url_for
from app.forms import AddMovieForm
from flask_login import current_user
from app.models import Movie
from . import bp as main
from app import app

@main.route('/', methods = ['GET', 'POST'])
def home():
    friday_pick = ''
    mf = AddMovieForm()
    if mf.validate_on_submit():
        if current_user.is_authenticated:
            movies = Movie.query.filter_by(title=mf.title.data).first()
            if movies and movies.if_recommended(mf.year.data):
                flash(f'{mf.title.data} has already been recommended!')
            else:
                movie = Movie(title = mf.title.data,
                              user_id = current_user.user_id,
                              release_year = str(mf.year.data),
                              description = mf.description.data,
                              )
                movie.commit()
                flash(f'{mf.title.data} has been added to the list!')
                return redirect(url_for('main.home'))
        else:
            flash(f"You need to make an account (<a href=\"auth/register\">here</a>) to recommend a movie <br>(Or login <a href=\"auth/signin\">here</a>)")
    return render_template('index.jinja', chosen=friday_pick, form=mf)