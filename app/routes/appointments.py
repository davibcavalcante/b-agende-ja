from flask import Blueprint, jsonify, request
from ..services.appointments_service import post_appointments
from ..middleware.auth import token_required

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointment', methods=['POST'])
@token_required
def post_appointments_bp(user):
    data = request.json
    response = post_appointments(data)

    if "error" in response:
        if "Validation error" in response["error"]:
            return jsonify(response), 400
        elif "Database insertion error" in response["error"]:
            return jsonify(response), 500
        else:
            return jsonify(response), 500
    
    return jsonify(response), 201