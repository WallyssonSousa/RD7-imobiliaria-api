from database import db

class Inquilino(db.Model):
    __tablename__ = 'inquilino'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), unique=True, nullable=False)

    contrato_inicio = db.Column(db.Date)
    contrato_fim = db.Column(db.Date)

    # Relacionamento reverso
    cliente = db.relationship('Cliente', back_populates='inquilino')