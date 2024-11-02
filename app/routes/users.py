from flask import Blueprint, jsonify, request
from services.user_service import get_users, login, register

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def get_users_route():
    return jsonify(get_users())

@users_bp.route('/login', methods=['POST'])
def login_route():
    data = request.json
    try:
        return jsonify(login(data)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/register', methods=['POST'])
def register_route():
    data = request.json
    try:
        return jsonify(register(data)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400