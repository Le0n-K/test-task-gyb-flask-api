from flask import Blueprint, request, jsonify, abort
from .models import User
from .database import db
from flasgger.utils import swag_from

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
@swag_from({
    "tags": ["Users"],
    "summary": "Getting a list of all users",
    "responses": {
        "200": {
            "description": "User list successfully retrieved"
        }
    }
})
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email, "created_at": u.created_at} for u in users
    ])


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@swag_from({
    "tags": ["Users"],
    "summary": "Getting information about a specific user",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "User information successfully received"
        },
        "404": {
            "description": "User not found"
        }
    }
})
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "name": user.name, "email": user.email, "created_at": user.created_at})


@user_bp.route("/users", methods=["POST"])
@swag_from({
    "tags": ["Users"],
    "summary": "Creating a new user",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "required": ["name", "email"],
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        "201": {
            "description": "User created successfully"
        },
        "400": {
            "description": "Data validation error or email already exists"
        }
    }
})
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400
    
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
    
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email, "created_at": user.created_at}), 201


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@swag_from({
    "tags": ["Users"],
    "summary": "Updating user data",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True
        },
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "User data successfully updated"
        },
        "400": {
            "description": "Data validation error or email already exists"
        },
        "404": {
            "description": "User not found"
        }
    }
})
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        if User.query.filter(User.email == data["email"], User.id != user_id).first():
            return jsonify({"error": "Email already exists"}), 400
        user.email = data["email"]

    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email, "created_at": user.created_at})


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Users"],
    "summary": "Deleting a user",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        "200": {
            "description": "User successfully deleted"
        },
        "404": {
            "description": "User not found"
        }
    }
})
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User Deleted"})
