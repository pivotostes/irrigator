import json
import os

ARQUIVO = "instance/sensores.txt"

def atualizar_sensores(args):
    try:
        dados = {
            "s1": int(args.get("s1")),
            "s2": int(args.get("s2")),
            "s3": int(args.get("s3")),
            "s4": int(args.get("s4")),
        }
    except (TypeError, ValueError):
        return "Parâmetros inválidos", 400

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

    return "Sensores Atualizados"
