from models.user_model import User
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from config import Config
from flask import current_app
import jwt
import datetime
import bcrypt

client = MongoClient(Config.MONGO_URI)
db = client['agendeja_db']
users_collection = db['users']

def create_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def get_users():
    users = users_collection.find()
    return [User(**user).dict(by_alias=True) for user in users]

def login(data):
    cpf = data['cpf']
    password = data['senha'].encode('utf-8')
    
    user = users_collection.find_one({"cpf": cpf})
    
    if user and bcrypt.checkpw(password, user['senha'].encode('utf-8')):
        token = create_token(str(user['_id']))
        return {'token': token, 'user_id': str(user['_id']), 'msg': 'Login bem-sucedido'}
    
    return {'error': 'Credenciais inválidas'}

def register(data):
    if users_collection.find_one({"cpf": data["cpf"]}):
        raise ValueError("CPF já existe!")

    hashed_password = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt(6))
    data['senha'] = hashed_password.decode('utf-8')

    user = User(**data)
    user_dict = user.dict(by_alias=True, exclude={"id"})
    
    try:
        result = users_collection.insert_one(user_dict)
        token = create_token(result.inserted_id)
        return {'id': str(result.inserted_id), 'token': token}
    except DuplicateKeyError:
        raise ValueError("Usuário já existe")