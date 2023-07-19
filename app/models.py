from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
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