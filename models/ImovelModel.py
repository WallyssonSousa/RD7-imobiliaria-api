from database import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum

class Imovel(db.Model):
    __tablename__ = "imoveis"

    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(9), nullable=False)  # formato 00000-000
    logradouro = db.Column(db.String(255))
    bairro = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    estado = db.Column(db.String(2))
    observacoes = db.Column(db.Text, nullable=True)  # descrição livre