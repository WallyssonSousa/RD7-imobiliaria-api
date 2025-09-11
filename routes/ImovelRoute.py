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
@jwt_required()
def criar_imovel():
    dados = request.get_json()

    # Lista de campos obrigatórios
    campos_obrigatorios = ["cep", "tipo_imovel", "metragem", "valor_aluguel", "valor_venda", "iptu", "finalidade"]
    campos_faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]
    if campos_faltando:
        return jsonify({"erro": "Campos obrigatórios faltando", "campos": campos_faltando}), 400

    cep = dados.get("cep")

    # Busca endereço no ViaCEP
    endereco = buscar_endereco_por_cep(cep)
    if not endereco:
        return jsonify({"erro": "CEP inválido ou não encontrado"}), 400

    # Cria objeto Imovel
    imovel = Imovel(
        tipo_imovel=dados.get("tipo_imovel"),
        cep=cep,
        logradouro=endereco.get("logradouro"),
        bairro=endereco.get("bairro"),
        cidade=endereco.get("localidade"),
        estado=endereco.get("uf"),
        complemento=dados.get("complemento"),

        metragem=dados.get("metragem"),
        quartos=dados.get("quartos"),
        suites=dados.get("suites"),
        banheiros=dados.get("banheiros"),
        vagas=dados.get("vagas"),

        valor_aluguel=dados.get("valor_aluguel"),
        valor_venda=dados.get("valor_venda"),
        condominio=dados.get("condominio"),
        iptu=dados.get("iptu"),

        finalidade=dados.get("finalidade"),
        disponivel=dados.get("disponivel", True),

        mobilia=dados.get("mobilia", "VAZIO"),
        observacoes=dados.get("observacoes")
    )

    # Salvar no banco
    db.session.add(imovel)
    db.session.commit()

    return jsonify({
        "mensagem": "Imóvel criado com sucesso!",
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
    }), 201
