from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .routes import routes_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(routes_blueprint)
    
    @app.route('/')
    def home():
        return jsonify(message="Servidor rodando!")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)