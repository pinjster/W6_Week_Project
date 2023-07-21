from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Movie, User
from . import bp as api

#create
@api.post('/create-movie')
@jwt_required()
def add_movie():
    info = request.json
    user = User.query.filter_by(username = get_jwt_identity()).first()
    try:
        u = User(user_id = user.user_id)
        u.from_dict(info)
        return jsonify(message= f"successfully added {info['title']}"), 200
    except:
        return jsonify(message= f"ERROR: could not add movie"), 400

#read
@api.get('/read-profile/<username>')
def get_user(username):
    user = User.query.filter_by(username = username).first()
    if user:
        return jsonify(user = user.to_dict())
    return jsonify(message= f'username {username} does not exist'), 400


@api.get('/top-pick')
def get_top_pick():
    top_pick = Movie.query.all()[0]
    if not top_pick:
        return jsonify(message= "ERROR: No movies have been recommended"), 400
    else:
        return jsonify({'top_pick' : top_pick.title})

@api.route('/read-current-user', methods = ['GET'])
def read_current_user():
    pass

#update
@api.route('/update-desc/<movie_id>', methods = ['PUT'])
@jwt_required
def edit_description(movie_id):
    movie = Movie.query.filter_by(movie_id = movie_id)
    if not movie:
        return jsonify(status = "ERROR: movie ID does not exist"), 400
    if movie.author.username != get_jwt_identity():
        return jsonify(status= "ERROR: You cannot edit this description"), 400
    movie.description = request.json.get('description')
    return jsonify(status= "Suggestion description successfully changed"), 200
    
@api.put('/update-top-pick')
@jwt_required()
def update_pick():
    pass

#delete
@api.delete('/del-movie/<movie_id>')
@jwt_required()
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    title = movie.title
    if not movie:
        return jsonify(status= 'movie ID dose not exist'), 400
    if movie.author.username != get_jwt_identity():
        return jsonify(status= 'You cannot remove this movie'), 400
    movie.delete_movie()
    return jsonify(status= f"{title} removed"), 200