from database import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    roles = db.Column(ARRAY(Enum("ADMIN", "USUARIO", "INQUILINO", "PROPRIETARIO", name="role_enum")), nullable=False, default=["USUARIO"]) # Perfis atribuídos ao usuário 
    token = db.Column(db.Text, nullable=True)  