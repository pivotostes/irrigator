from flask import Blueprint, request, jsonify
import json
from app.services.bombas_service import get_estado_bombas, alterar_estado_bomba, inicializar_bombas


bombas_bp = Blueprint('bombas', __name__)

inicializar_bombas()

# GET - retorna estados atuais das bombas
@bombas_bp.route('/estado_bombas', methods=['GET'])
def estado_bombas():
    return get_estado_bombas()

# POST - altera o estado de uma bomba específica
@bombas_bp.route('/estado_bombas/<int:id>', methods=['POST'])
def controla_bomba(id):
    return alterar_estado_bomba(id)