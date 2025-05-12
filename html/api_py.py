from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

SENSORES_FILE = "sensores.txt"
BOMBAS_FILE = "bomba_estado.txt"


@app.route("/atualizar_sensores", methods=["GET"])
def atualizar_sensores():
    try:
        s1 = int(request.args.get("s1"))
        s2 = int(request.args.get("s2"))
        s3 = int(request.args.get("s3"))
        s4 = int(request.args.get("s4"))
    except (TypeError, ValueError):
        return "Parâmetros inválidos", 400

    dados = {"s1": s1, "s2": s2, "s3": s3, "s4": s4}

    with open(SENSORES_FILE, "w") as f:
        json.dump(dados, f)

    return "Sensores Atualizados"


@app.route("/estado_bombas", methods=["GET"])
def estado_bombas():
    if os.path.exists(BOMBAS_FILE):
        with open(BOMBAS_FILE, "r") as f:
            try:
                estados = json.load(f)
            except json.JSONDecodeError:
                estados = {}
    else:
        estados = {}

    return jsonify(estados)


@app.route("/controlar_bomba", methods=["POST"])
def controlar_bomba():
    data = request.get_json()
    if not data or "bomba" not in data or "estado" not in data:
        return "JSON com 'bomba' e 'estado' é obrigatório", 400

    try:
        bomba = int(data["bomba"])
        estado = int(data["estado"])
    except ValueError:
        return "Valores inválidos para 'bomba' ou 'estado'", 400

    if os.path.exists(BOMBAS_FILE):
        with open(BOMBAS_FILE, "r") as f:
            try:
                estados = json.load(f)
            except json.JSONDecodeError:
                estados = {}
    else:
        estados = {}

    estados[str(bomba)] = estado

    with open(BOMBAS_FILE, "w") as f:
        json.dump(estados, f)

    return f"Bomba {bomba} {'Ligada' if estado else 'Desligada'}"


@app.errorhandler(404)
def rota_invalida(e):
    return "Rota não encontrada", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
