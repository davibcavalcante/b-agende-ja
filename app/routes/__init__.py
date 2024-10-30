from flask import Blueprint
from .users import users_bp

routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.register_blueprint(users_bp)
