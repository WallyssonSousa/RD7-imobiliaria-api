from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Métodos utilitários
    def set_senha(self, senha):
        """Gera hash seguro para a senha antes de salvar no banco."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        """Verifica se a senha informada confere com o hash."""
        return check_password_hash(self.senha_hash, senha)