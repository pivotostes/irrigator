from flask import Blueprint, request, jsonify
from app.services.bombas_service import obter_estado_bombas, controlar_bomba

bombas_bp = Blueprint('bombas', __name__)

@bombas_bp.route("/estado_bombas", methods=["GET"])
def estado():
    return obter_estado_bombas()

@bombas_bp.route("/controlar_bomba", methods=["POST"])
def controlar():
    return controlar_bomba(request.get_json())
