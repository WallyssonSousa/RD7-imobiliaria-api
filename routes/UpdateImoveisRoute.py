from flask import request, jsonify
from database import db
from routes.ImovelRoute import buscar_endereco_por_cep
from routes.ImovelRoute import imovel_bp
from models.ImovelModel import Imovel
from flask_jwt_extended import jwt_required

@imovel_bp.route("/imoveis/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_imovel(id):
    dados = request.get_json()

    # Busca o imóvel existente
    imovel = Imovel.query.get(id)
    if not imovel:
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    # Campos que podem ser atualizados
    campos_permitidos = [
        "tipo_imovel", "cep", "complemento", "metragem", "quartos", "suites", 
        "banheiros", "vagas", "valor_aluguel", "valor_venda", "condominio", "iptu",
        "finalidade", "disponivel", "mobilia", "observacoes"
    ]

    # Atualiza os campos permitidos
    for campo in campos_permitidos:
        if campo in dados:
            setattr(imovel, campo, dados[campo])

    # Se CEP for atualizado, busca endereço
    if "cep" in dados:
        endereco = buscar_endereco_por_cep(dados["cep"])
        if not endereco:
            return jsonify({"erro": "CEP inválido ou não encontrado"}), 400
        
        imovel.logradouro = endereco.get("logradouro")
        imovel.bairro = endereco.get("bairro")
        imovel.cidade = endereco.get("localidade")
        imovel.estado = endereco.get("uf")

    # Salva alterações
    db.session.commit()

    return jsonify({
        "mensagem": "Imóvel atualizado com sucesso!",
        "imovel": {
            "id": imovel.id,
            "tipo_imovel": imovel.tipo_imovel,
            "cep": imovel.cep,
            "logradouro": imovel.logradouro,
            "bairro": imovel.bairro,
            "cidade": imovel.cidade,
            "estado": imovel.estado,
            "finalidade": imovel.finalidade,
            "mobilia": imovel.mobilia,
            "observacoes": imovel.observacoes
        }
    }), 200
