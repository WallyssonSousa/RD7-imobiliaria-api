from flask import Blueprint, request, jsonify
from database import db
from models.ClienteModel import Cliente
from email_validator import validate_email, EmailNotValidError

cadastro_bp = Blueprint('cadastro', __name__)

@cadastro_bp.route('/cadastro', methods=['POST'])
def cadastrar_cliente():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({"error": "Preencha todos os campos (nome, email, senha)."}), 400

    try:
        # Validação completa do e-mail
        email_validado = validate_email(email)
        email = email_validado.email
    except EmailNotValidError:
        return jsonify({"error": "E-mail inválido. Verifique e tente novamente."}), 400

    if Cliente.query.filter_by(email=email).first():
        return jsonify({"error": "E-mail já cadastrado."}), 400

    novo_cliente = Cliente(nome=nome, email=email)
    novo_cliente.set_senha(senha)

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({
        "message": "Cliente cadastrado com sucesso!",
        "cliente": {
            "id": novo_cliente.id,
            "nome": novo_cliente.nome,
            "email": novo_cliente.email
        }
    }), 201
