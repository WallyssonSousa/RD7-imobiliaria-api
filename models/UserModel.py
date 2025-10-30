from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.Column(db.ARRAY(db.String), default=["USUARIO"])

    def set_password(self, senha):
        self.password_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.password_hash, senha)
