import json
import os

ARQUIVO = "instance/bomba_estado.txt"

def obter_estado_bombas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            try:
                estados = json.load(f)
            except json.JSONDecodeError:
                estados = {}
    else:
        estados = {}
    return jsonify(estados)

def controlar_bomba(data):
    if not data or "bomba" not in data or "estado" not in data:
        return "JSON com 'bomba' e 'estado' é obrigatório", 400

    try:
        bomba = int(data["bomba"])
        estado = int(data["estado"])
    except ValueError:
        return "Valores inválidos", 400

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            try:
                estados = json.load(f)
            except json.JSONDecodeError:
                estados = {}
    else:
        estados = {}

    estados[str(bomba)] = estado

    with open(ARQUIVO, "w") as f:
        json.dump(estados, f)

    return f"Bomba {bomba} {'Ligada' if estado else 'Desligada'}"
