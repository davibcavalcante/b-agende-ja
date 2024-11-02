from flask import request, jsonify
from functools import wraps
import jwt
from config import Config

def verify_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token é necessário!'}), 401

        user = verify_token(token)
        if user is None:
            return jsonify({'message': 'Token inválido ou expirado!'}), 401

        return f(user, *args, **kwargs)
    return decorated
