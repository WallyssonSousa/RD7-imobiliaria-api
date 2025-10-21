from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.ClienteModel import Cliente

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/cliente/<int:cliente_id>", methods=["GET"])
@jwt_required()
def get_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    cliente_data = {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "criado_em": cliente.criado_em.isoformat(),
        "funcoes": {
            "funcionario": bool(cliente.funcionario),
            "inquilino": bool(cliente.inquilino),
            "proprietario": bool(cliente.proprietario)
        }
    }

    return jsonify(cliente_data), 200