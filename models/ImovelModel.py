from database import db
from sqlalchemy import Enum
import datetime

class Imovel(db.Model):
    __tablename__ = "imoveis"

    id = db.Column(db.Integer, primary_key=True)
    tipo_imovel = db.Column(Enum("CASA", "APARTAMENTO", "TERRENO", "SALA_COMERCIAL", name="tipo_imovel_enum"), nullable=False, default="CASA")
    
    cep = db.Column(db.String(9), nullable=False)
    logradouro = db.Column(db.String(255))
    bairro = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    estado = db.Column(db.String(2))
    complemento = db.Column(db.String(255))

    metragem = db.Column(db.String(50))
    quartos = db.Column(db.Integer)
    suites = db.Column(db.Integer)
    banheiros = db.Column(db.Integer)
    vagas = db.Column(db.Integer)

    valor_aluguel = db.Column(db.Numeric(10,2))
    valor_venda = db.Column(db.Numeric(12,2))
    condominio = db.Column(db.Numeric(10,2))
    iptu = db.Column(db.Numeric(10,2))

    finalidade = db.Column(Enum("ALUGUEL", "COMPRA", "AMBOS", name="finalidade_enum"), nullable=False, default="AMBOS")
    disponivel = db.Column(db.Boolean, default=True)

    mobilia = db.Column(Enum("MOBILIADO", "SEMIMOBILIADO", "VAZIO", name="mobilia_enum"), default="VAZIO")
    observacoes = db.Column(db.Text, nullable=True)

    data_cadastro = db.Column(db.DateTime, default=datetime.datetime.utcnow)
