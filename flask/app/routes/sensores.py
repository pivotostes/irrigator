# app/routes/sensores.py
from flask import Blueprint, jsonify
import json
import os

sensores_bp = Blueprint('sensores', __name__)

@sensores_bp.route("/estado_sensores", methods=["GET"])
def estado_sensores():
    ARQUIVO = "instance/sensores.txt"
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            try:
                sensores = json.load(f)
            except json.JSONDecodeError:
                sensores = {}
    else:
        sensores = {}

    return jsonify(sensores)
