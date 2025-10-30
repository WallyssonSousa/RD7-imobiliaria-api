from database import db

class Funcionario(db.Model):
    __tablename__ = 'funcionario'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), unique=True, nullable=False)

    # Campos específicos de funcionário
    cargo = db.Column(db.String(100))
    setor = db.Column(db.String(100))

    # Relacionamento reverso
    cliente = db.relationship('Cliente', back_populates='funcionario')