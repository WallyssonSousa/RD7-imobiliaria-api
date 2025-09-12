from flask import jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.ImovelModel import Imovel
from routes.ImovelRoute import imovel_bp

@imovel_bp.route("/imoveis/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_imovel(id):
    # Busca o imóvel pelo ID
    imovel = Imovel.query.get(id)
    if not imovel:
        return jsonify({"erro": "Imóvel não encontrado"}), 404
    
    # Remove do banco
    db.session.delete(imovel)
    db.session.commit()
    
    return jsonify({"mensagem": f"Imóvel com ID {id} deletado com sucesso."}), 200