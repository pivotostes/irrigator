from flask import Blueprint, request
from app.services.sensores_service import atualizar_sensores

sensores_bp = Blueprint('sensores', __name__)

@sensores_bp.route("/atualizar_sensores", methods=["GET"])
def atualizar():
    return atualizar_sensores(request.args)
