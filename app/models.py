from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(80), nullable = False, unique = True)
    pass_hash = db.Column(db.String(), nullable = False)
    suggestions = db.relationship('Movie', backref = 'author', lazy = True)
    voted = db.relationship('Vote', backref = 'voter', lazy = True)

    def __repr__(self):
        return f'USER: {self.username}'
    
    def get_id(self):
        return str(self.user_id)

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, d):
        self.fname = d['fname']
        self.lname  = d['lname']
        self.username  = d['username']
        self.email  = d['email']
        self.pass_hash  = d['pass_hash']
        self.hash_password(self.pass_hash)   

    def to_dict(self):
        d = {
            'user_id' : self.user_id,
            'fname' : self.fname,
            'lname' : self.lname,
            'username' : self.username,
            'email' : self.email
        }
        return d     

class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    release_year = db.Column(db.String(4) , nullable = True)
    rated = db.Column(db.String() , nullable = True)
    description = db.Column(db.String() , nullable = True)
    poster = db.Column(db.String() , nullable = True)
    votes = db.relationship('Vote', backref = 'voted_on', lazy = True)


    def __repr__(self):
        return f'{self.title}'
    
    def if_recommended(self, year):
        return True if self.release_year == str(year) else False
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_movie(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        d = {
            'movie_id' : self.movie_id,
            'title' : self.title,
            'user_id' : self.user_id,
            'date_added' : self.date_added,
            'release_year' : self.release_year,
            'rated' : self.rated,
            'description' : self.description,
            'poster' : self.poster
        }
        return d    
    
    def from_dict(self, d):
        self.title = d['title']
        self.user_id = d['user_id']
        self.release_year = d['release_year']
        self.rated = d['rated']
        self.description = d['description']
        self.poster = d['poster']
    
class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    vote_value = db.Column(db.Boolean, nullable = False)
    movie_id =db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable = False)

    def __repr__(self):
        return f'{self.voter.username} voted {"for" if self.vote_value else "against"} {self.voted_on.title}'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_vote(self):
        db.session.delete(self)
        db.session.commit()


