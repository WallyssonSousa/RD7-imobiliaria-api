from database import db

class Proprietario(db.Model):
    __tablename__ = 'proprietario'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), unique=True, nullable=False)

    cpf = db.Column(db.String(14))
    telefone = db.Column(db.String(20))

    # Relacionamento reverso
    cliente = db.relationship('Cliente', back_populates='proprietario')