from flask import jsonify, request
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, get_jwt_identity
from app.models import User
from flask_login import login_user
from . import bp as api

#create
@api.route('/create-user', methods = ['POST'])
def add_user():
    info = request.json
    response = {}
    if User.query.filter_by(username = info['username']).first():
        response['username error'] = f"{info['username']} is already in use" 
    if User.query.filter_by(email = info['email']).first():
        response['email error'] = f"{info['email']} is already in use" 
    if 'pass_hash' not in info:
        response['password error'] = 'please include password'
    try:
        u = User()
        u.from_dict(info)
        u.commit()
        login_user(u)
        return jsonify({'update' : f'{u.username} has been registered'}), 200
    except:
        return jsonify(response), 400

@api.post('/signin')
def signin():
    username = request.json.get('username')
    pass_hash = request.json.get('password')
    user = User.query.filter_by(username = username).first()
    if user and user.check_password(pass_hash):
        access_token = create_access_token(identity= username)
        return jsonify({'access_token' : access_token},
                       {'status' : f'{username} succesfully logged in'}), 200
    else:
        return jsonify({'message': "Invalid Username or Password / Try Again"}), 400
        

@api.post('/logout')
def logout():
    response = jsonify({'message' : 'Successfully logged out'}), 200
    unset_jwt_cookies(response)
    return response

#read
@api.get('/read-users')
def get_users():
    u = User.query.all()
    return jsonify({'users' : [user.to_dict() for user in u]})

#delete
@api.route('/del-user/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status' : 'ERROR: user ID not valid'})
    if user.username != get_jwt_identity():
        return jsonify({'status' : 'Cannot delete this user'})
    user.delete()
    return jsonify({'status' : 'SUCCESS: user deleted'})
    