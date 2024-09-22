from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('authentication', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        return jsonify({'message': 'Username is required'}), 400
    if not password:
        return jsonify({'message': 'Password is required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500

    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def authenticate_user():
    username = request.json.get('username')
    password = request.json.get('password')

    existing_user = User.query.filter_by(username=username).first()
    
    if not existing_user or not existing_user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=existing_user.id)
    return jsonify({'access_token': access_token}), 200
