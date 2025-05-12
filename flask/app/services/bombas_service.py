from flask import request, jsonify
import json
import os

BOMBAS_FILE = os.path.join('instance', 'bombas_estado.txt')


# Garante que o arquivo exista com todas bombas desligadas
def inicializar_bombas():
    if not os.path.exists(BOMBAS_FILE):
        estados_iniciais = {str(i): 0 for i in range(1, 5)}
        with open(BOMBAS_FILE, 'w') as f:
            json.dump(estados_iniciais, f)


# Retorna o estado atual das bombas
def get_estado_bombas():
    if os.path.exists(BOMBAS_FILE):
        with open(BOMBAS_FILE, "r") as f:
            try:
                estados = json.load(f)
            except json.JSONDecodeError:
                estados = {}
    else:
        estados = {}
    return jsonify(estados)


# Altera o estado de uma bomba específica
def alterar_estado_bomba(id):
    if not 1 <= id <= 4:
        return jsonify({"erro": "ID da bomba deve estar entre 1 e 4"}), 400

    data = request.get_json()
    if not data or "estado" not in data:
        return jsonify({"erro": "Corpo JSON com 'estado' é obrigatório"}), 400

    estado = int(data["estado"])
    if estado not in [0, 1]:
        return jsonify({"erro": "Estado deve ser 0 ou 1"}), 400

    # Carrega o estado atual e atualiza
    with open(BOMBAS_FILE, 'r') as f:
        estados = json.load(f)

    estados[str(id)] = estado

    with open(BOMBAS_FILE, 'w') as f:
        json.dump(estados, f)

    return jsonify({str(id): estado})
