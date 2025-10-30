import requests
from flask import Blueprint

# Criação do Blueprint na rota principal
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


