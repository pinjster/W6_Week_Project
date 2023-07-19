from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    fname = StringField('First name')
    lname = StringField('Last name')
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Your email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    reenter_password = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class AddMovieForm(FlaskForm):
    title = StringField('Movie title', validators = [DataRequired()])
    year = IntegerField('Year?')
    description = TextAreaField('Reason for suggestion')
    submit = SubmitField('Submit suggestion')

class VoteForm(FlaskForm):
    option = SelectField(u'Vote', choices=['upvote', 'downvote'])
    submit = SubmitField('vote')