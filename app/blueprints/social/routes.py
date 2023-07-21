from app import app
from flask import g, flash, render_template, redirect, url_for
from app.forms import VoteForm, AddMovieForm, DeleteForm, SearchUserForm
from app.models import Movie, User
from flask_login import current_user, login_required
from . import bp

@app.before_request
def before_request():
    g.vf = VoteForm()
    g.amf = AddMovieForm()
    g.df = DeleteForm()
    g.suf = SearchUserForm()

@bp.route('/suggested')
def suggested():
    movie_list = Movie.query.all()
    return render_template('suggested.jinja', movie_list=movie_list, form=g.vf)

@bp.route('/about')
def about():
    return render_template('about.jinja')

@bp.route('/my_profile', methods = ['GET', 'POST'])
@login_required
def my_profile():
    if g.df.validate_on_submit():
        flash(f"{g.df.name.data} has been removed from your recommendations")
        mov = Movie.query.filter_by(movie_id = g.df.item.data).first()
        Movie.delete_movie(mov)
        
    return render_template('my_profile.jinja', movie_list = Movie.query.filter_by(user_id = current_user.user_id), form = g.df)

@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        suggestions = user.suggestions
        return render_template('profile.jinja', username = username, searchform = g.suf, posts = suggestions)
    else:
        flash(f'{username} does not exist')
        return redirect(url_for('main.home'))

@bp.post('/usersearch')
def usersearch():
        return redirect(url_for('social.profile', username = g.suf.username.data))