from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models.UserModel import User
from models.FuncionarioModel import Funcionario
from models.InquilinoModel import Inquilino
from models.ProprietarioModel import Proprietario
from database import db  # ou 'from extensions import db' se estiver usando extensions.py

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    # Verifica role do usuário logado
    claims = get_jwt()
    role = claims.get("role")

    if role != "admin":
        return jsonify({"erro": "Acesso negado. Apenas administradores podem acessar esta rota."}), 403

    # Busca todos os usuários
    users = User.query.all()

    # Monta a resposta JSON
    users_list = []
    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "funcoes": {
                "funcionario": bool(user.funcionario),
                "inquilino": bool(user.inquilino),
                "proprietario": bool(user.proprietario)
            }
        })

    return jsonify(users_list), 200