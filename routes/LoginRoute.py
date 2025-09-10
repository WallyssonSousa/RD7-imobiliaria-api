from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from datetime import timedelta
from flask_jwt_extended import JWTManager

login_bp = Blueprint("login", __name__)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "defaultsecret")

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    JWTManager(app)
    

@login_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    username = dados.get("username")
    password = dados.get("password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        role = "admin"
        token = create_access_token(identity={"username": username, "role": "admin"})
        return jsonify({"mensagem": "Login realizado com sucesso", "token": token, "role": role}), 200

    return jsonify({"erro": "Credenciais inválidas"}), 401

