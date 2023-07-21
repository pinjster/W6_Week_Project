from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    fname = StringField('First name')
    lname = StringField('Last name')
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Your email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    reenter_password = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class AddMovieForm(FlaskForm):
    title = StringField('Movie title', validators = [DataRequired()])
    year = IntegerField('Year?')
    description = TextAreaField('Reason for suggestion')
    submit = SubmitField('Submit suggestion')
    
class DeleteForm(FlaskForm):
    item = HiddenField()
    name = HiddenField()
    del_form = SubmitField('Delete')

class SearchUserForm(FlaskForm):
    username = StringField('Username', validators=[ DataRequired() ])
    submit = SubmitField('Search')

class VoteForm(FlaskForm):
    option = SelectField('Vote', choices=['upvote', 'downvote'])
    submit = SubmitField('vote')

