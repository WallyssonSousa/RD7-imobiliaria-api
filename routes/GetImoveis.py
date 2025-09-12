from routes.ImovelRoute import imovel_bp
from flask import jsonify
from models.ImovelModel import Imovel
from flask_jwt_extended import jwt_required

@imovel_bp.route("/imoveis", methods=["GET"])
@jwt_required()
def listar_imoveis():
    imoveis = Imovel.query.order_by(Imovel.id.asc()).all() #permite a ordenação por ID (1, 2, 3...)
    
    resultado = []
    for imovel in imoveis:
        resultado.append({
           "id": imovel.id,
            "tipo_imovel": imovel.tipo_imovel,
            "cep": imovel.cep,
            "logradouro": imovel.logradouro,
            "bairro": imovel.bairro,
            "cidade": imovel.cidade,
            "estado": imovel.estado,
            "metragem": imovel.metragem,
            "quartos": imovel.quartos,
            "suites": imovel.suites,
            "banheiros": imovel.banheiros,
            "vagas": imovel.vagas,
            "valor_aluguel": imovel.valor_aluguel,
            "valor_venda": imovel.valor_venda,
            "condominio": imovel.condominio,
            "iptu": imovel.iptu,
            "finalidade": imovel.finalidade,
            "disponivel": imovel.disponivel,
            "mobilia": imovel.mobilia,
            "observacoes": imovel.observacoes 
        })
        
    return jsonify(
        resultado
    ), 200