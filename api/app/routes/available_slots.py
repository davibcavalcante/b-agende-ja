from flask import Blueprint, jsonify, request
from ..services.available_slots_service import get_available_slots, delete_available_slots
from ..middleware.auth import token_required

available_slots_bp = Blueprint('available_slots', __name__)

@available_slots_bp.route('/availableslots', methods=['GET'])
@token_required
def get_available_slots_route(user):
    try:
        return jsonify(get_available_slots()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@available_slots_bp.route('/availableslots', methods=['DELETE'])
@token_required
def delete_available_slots_route(user):
    data = request.json
    response = delete_available_slots(data)
    
    if 'error' in response:
        status_code = 400 if "ID Inválido" in response['error'] else 404
        return jsonify(response), status_code
    else:
        return jsonify(response), 200