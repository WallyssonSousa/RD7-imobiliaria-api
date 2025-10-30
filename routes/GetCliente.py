# routes/GetClientes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models.ClienteModel import Cliente

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/clientes", methods=["GET"])
@jwt_required()
def get_clientes():
    # Verifica role do usuário logado (opcional: permitir só admin acessar)
    claims = get_jwt()
    role = claims.get("role")
    if role != "admin":
        return jsonify({"erro": "Acesso negado. Apenas administradores podem acessar esta rota."}), 403

    clientes = Cliente.query.all()
    clientes_list = []
    for cliente in clientes:
        clientes_list.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "criado_em": cliente.criado_em.isoformat()
        })

    return jsonify(clientes_list), 200
