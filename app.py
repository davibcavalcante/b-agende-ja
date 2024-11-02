from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from .app.config import Config
from app.routes import routes_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    jwt = JWTManager(app)

    app.register_blueprint(routes_blueprint)
    
    @app.route('/')
    def home():
        return jsonify(message="Servidor rodando!")

    return app

if __name__ == '__main__':
    app = create_app()

    app.run()