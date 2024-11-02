from flask import Blueprint

routes_blueprint = Blueprint('routes', __name__)

from .users import users_bp
from .available_slots import available_slots_bp
from .appointments import appointments_bp

routes_blueprint.register_blueprint(users_bp)
routes_blueprint.register_blueprint(available_slots_bp)
routes_blueprint.register_blueprint(appointments_bp)