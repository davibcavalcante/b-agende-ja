from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.routes import routes_blueprint

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

app.register_blueprint(routes_blueprint)
    
@app.route('/')
def home():
    return jsonify(message="Servidor rodando!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
