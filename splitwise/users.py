# user.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
from datetime import datetime, timedelta
from pymongo import MongoClient
import uuid
from db_init import db

# MongoDB Configuration
database = db
users_collection = db.users

# Create a Blueprint for user routes
user_bp = Blueprint('user_bp', __name__)
user_bp.config["JWT_SECRET_KEY"] = "test123"  # Replace with a secure secret
user_bp.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Token expires in 1 hour
jwt = JWTManager(user_bp)



# Register a new user
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # Check for required fields
    if not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password are required"}), 400

    # Check if the user already exists
    if users_collection.find_one({"username": data["username"]}):
        return jsonify({"message": "User already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

    # Save the user to the database
    users_collection.insert_one({
        "username": data["username"],
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

    return jsonify({"message": "User registered successfully"}), 201

# Login a user and return a JWT
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    # Check for required fields
    if not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password are required"}), 400

    # Find the user in the database
    user = users_collection.find_one({"username": data["username"]})
    if not user:
        return jsonify({"message": "Invalid username or password"}), 401

    # Verify the password
    if not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        return jsonify({"message": "Invalid username or password"}), 401

    # Generate a JWT
    access_token = create_access_token(identity={"username": data["username"]})

    return jsonify({"message": "Login successful", "access_token": access_token}), 200

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    # Get the current logged-in user
    current_user = get_jwt_identity()
    users = users_collection.find({}, {"_id": 0, "username": 1, "created_at": 1})

    return jsonify({
        "current_user": current_user,
        "users": list(users)
    }), 200


# Route to delete one the users
@user_bp.route('/users/', methods=['DELETE'])
def delete_all_user():
    try:
        # get users
        result = users_collection.delete_many({})

        if result.deleted_count > 0:
            return jsonify({"message": f"All User has deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Invalid user ID format", "error": str(e)}), 400



# Route to delete one the users
@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # get users
        result = users_collection.delete_one({"_id": user_id})

        if result.deleted_count == 1:
            return jsonify({"message": f"User with id {user_id} deleted successfully"}), 200
        else:
            return jsonify({"message": f"No user found with id {user_id}"}), 404
    except Exception as e:
        return jsonify({"message": "Invalid user ID format", "error": str(e)}), 400
