from flask import Blueprint, request, jsonify
from models.ClienteModel import Cliente
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

login_cliente_bp = Blueprint("login_cliente", __name__)

@login_cliente_bp.route("/login_cliente", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"error": "Preencha email e senha"}), 400

    usuario = Cliente.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"error": "Email ou senha inválidos"}), 401

    access_token = create_access_token(identity=usuario.id)
    return jsonify({"access_token": access_token}), 200
