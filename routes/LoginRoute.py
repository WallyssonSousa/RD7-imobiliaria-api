from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager
from models.ClienteModel import Cliente
from werkzeug.security import check_password_hash
import os
from datetime import timedelta

login_bp = Blueprint("login", __name__)

# Configurações de variáveis de ambiente
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "defaultsecret")

# Inicializa o JWT no app principal
def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    JWTManager(app)

@login_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    username = dados.get("username") or dados.get("email")  # aceita username ou email
    password = dados.get("password") or dados.get("senha")  # aceita password ou senha

    if not username or not password:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    # 1️⃣ Tentativa de login como ADMIN
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        token = create_access_token(identity=username, additional_claims={"role": "admin"})
        return jsonify({
            "mensagem": "Login de administrador realizado com sucesso",
            "token": token,
            "role": "admin"
        }), 200

    # 2️⃣ Tentativa de login como CLIENTE (usuário do banco)
    usuario = Cliente.query.filter_by(email=username).first()
    if usuario and usuario.verificar_senha(password):
        token = create_access_token(identity=usuario.id, additional_claims={"role": "cliente"})
        return jsonify({
            "mensagem": "Login de cliente realizado com sucesso",
            "token": token,
            "role": "cliente"
        }), 200

    # 3️⃣ Falha no login
    return jsonify({"erro": "Credenciais inválidas"}), 401
