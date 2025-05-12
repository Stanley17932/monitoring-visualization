from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
from extensions import mongo
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        print(f"MongoDB instance: {mongo.db}")
        data = request.json
        
        # Check if user already exists
        if mongo.db.users.find_one({'email': data['email']}):
            return jsonify({'message': 'Email already registered'}), 400
        
        user = {
            'username': data['username'],
            'email': data['email'],
            'password': generate_password_hash(data['password']),
            'role': 'user',  # Default role
            'created_at': datetime.utcnow()
        }
        
        mongo.db.users.insert_one(user)
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500


@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({'email': data['email']})
    
    if user and check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(current_user_id)})
    
    if user:
        return jsonify({
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'created_at': user['created_at']
        })
    
    return jsonify({'message': 'User not found'}), 404

@auth.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    data = request.json
    
    # Don't allow role updates through this endpoint
    if 'role' in data:
        del data['role']
    
    # Hash password if it's being updated
    if 'password' in data:
        data['password'] = generate_password_hash(data['password'])
    
    result = mongo.db.users.update_one(
        {'_id': ObjectId(current_user_id)},
        {'$set': data}
    )
    
    if result.modified_count:
        return jsonify({'message': 'Profile updated successfully'})
    return jsonify({'message': 'User not found'}), 404