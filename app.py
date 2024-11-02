from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.config import Config
from app.routes.users import users_bp
from app.routes.available_slots import available_slots_bp
from app.routes.appointments import appointments_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    jwt = JWTManager(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(available_slots_bp)
    app.register_blueprint(appointments_bp)
    
    @app.route('/')
    def home():
        return jsonify(message="Servidor rodando!")

    return app

if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)