import requests
from flask import Blueprint, request, jsonify
from database import db
from models.ImovelModel import Imovel
from flask_jwt_extended import jwt_required

imovel_bp = Blueprint("imoveis", __name__)

# Função auxiliar para buscar dados no ViaCEP
def buscar_endereco_por_cep(cep):
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if response.status_code == 200:
            dados = response.json()
            if "erro" in dados:
                return None
            return dados
    except Exception:
        return None
    return None

@imovel_bp.route("/imoveis", methods=["POST"])
@jwt_required()  # só usuário autenticado pode cadastrar
def criar_imovel():
    dados = request.get_json()

    cep = dados.get("cep")
    observacoes = dados.get("observacoes", "")

    if not cep:
        return jsonify({"erro": "O campo 'cep' é obrigatório"}), 400

    # Busca endereço pelo CEP
    endereco = buscar_endereco_por_cep(cep)
    if not endereco:
        return jsonify({"erro": "CEP inválido ou não encontrado"}), 400

    # Cria novo imóvel
    imovel = Imovel(
        cep=cep,
        logradouro=endereco.get("logradouro"),
        bairro=endereco.get("bairro"),
        cidade=endereco.get("localidade"),
        estado=endereco.get("uf"),
        observacoes=observacoes
    )

    db.session.add(imovel)
    db.session.commit()

    return jsonify({
        "id": imovel.id,
        "cep": imovel.cep,
        "logradouro": imovel.logradouro,
        "bairro": imovel.bairro,
        "cidade": imovel.cidade,
        "estado": imovel.estado,
        "observacoes": imovel.observacoes
    }), 201
