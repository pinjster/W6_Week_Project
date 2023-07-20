from flask_login import login_user, logout_user, current_user
from flask import g, flash, redirect, url_for, render_template
from . import bp as auth
from app.forms import LoginForm, RegisterForm
from app.models import User

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    lf = LoginForm()
    if lf.validate_on_submit():
        users = User.query.filter_by(email=lf.email.data).first()
        if users and users.check_password(lf.password.data):
            login_user(users)
            flash(f'{lf.email.data} logged in!')
            return redirect(url_for('main.home'))
        else:
            flash(f'Invalid User Data, Try Again')
    return render_template('signin.jinja', form=lf)

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    rf = RegisterForm()
    if rf.validate_on_submit():
        user_filter = User.query.filter_by(username=rf.username.data).first()
        email_filter = User.query.filter_by(email=rf.email.data).first()
        if user_filter or email_filter:
            flash(f"Username or Email already taken. Please Sign in <a href='signin'>here</a>.")
        else:
            user = User(fname=rf.fname.data, 
                        lname=rf.lname.data, 
                        username=rf.username.data, 
                        email=rf.email.data)
            user.hash_password(rf.password.data)
            user.commit()
            print(user)
            flash(f'{rf.fname.data if rf.fname.data else rf.username.data} registered')
            login_user(user)
            return redirect('/')
    return render_template('register.jinja', form=rf)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))