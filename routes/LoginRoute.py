from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import check_password_hash
from datetime import timedelta
import os

from database import db
from models.ClienteModel import Cliente  

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
        token = create_access_token(
            identity=username,
            additional_claims={"role": role}
        )
        return jsonify({
            "mensagem": "Login realizado com sucesso (admin)",
            "token": token,
            "role": role
        }), 200

    cliente = Cliente.query.filter_by(email=username).first()

    if cliente and cliente.verificar_senha(password):
        role = "cliente"
        token = create_access_token(
            identity=cliente.email,
            additional_claims={"role": role, "id": cliente.id}
        )
        return jsonify({
            "mensagem": "Login realizado com sucesso (cliente)",
            "token": token,
            "role": role,
            "cliente": {
                "id": cliente.id,
                "nome": cliente.nome,
                "email": cliente.email
            }
        }), 200

    return jsonify({"erro": "Credenciais inválidas"}), 401
