from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from database import db
from models.ClienteModel import Cliente
from models.FuncionarioModel import Funcionario
from models.InquilinoModel import Inquilino
from models.ProprietarioModel import Proprietario

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/atribuir_funcao", methods=["POST"])
@jwt_required()
def atribuir_funcao_cliente():
    # Pega as claims do JWT
    claims = get_jwt()
    role = claims.get("role")

    if role != "admin":
        return jsonify({"erro": "Acesso negado. Apenas administradores podem atribuir funções."}), 403

    data = request.get_json()
    cliente_id = data.get("cliente_id")
    funcao = data.get("funcao")

    if not cliente_id or not funcao:
        return jsonify({"erro": "Informe cliente_id e funcao"}), 400

    # Busca o cliente
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    funcao = funcao.lower()
    if funcao not in ["funcionario", "inquilino", "proprietario"]:
        return jsonify({"erro": "Função inválida. Use funcionario, inquilino ou proprietario"}), 400

    # Checa se já existe a função e cria a associação
    if funcao == "funcionario":
        if cliente.funcionario:
            return jsonify({"erro": "Cliente já é funcionário"}), 400
        novo = Funcionario(cliente_id=cliente.id)
    elif funcao == "inquilino":
        if cliente.inquilino:
            return jsonify({"erro": "Cliente já é inquilino"}), 400
        novo = Inquilino(cliente_id=cliente.id)
    elif funcao == "proprietario":
        if cliente.proprietario:
            return jsonify({"erro": "Cliente já é proprietário"}), 400
        novo = Proprietario(cliente_id=cliente.id)

    # Salva no banco
    db.session.add(novo)
    db.session.commit()

    # Atualiza o objeto cliente para refletir a nova função
    db.session.refresh(cliente)

    # Gera um dicionário das funções atuais
    funcoes_atuais = {
        "funcionario": bool(cliente.funcionario),
        "inquilino": bool(cliente.inquilino),
        "proprietario": bool(cliente.proprietario)
    }

    return jsonify({
        "mensagem": f"Função '{funcao}' atribuída com sucesso ao cliente '{cliente.nome}'.",
        "cliente_id": cliente.id,
        "funcoes_atuais": funcoes_atuais
    }), 200