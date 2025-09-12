import os
from flask import Flask 
from config import configure_app
from database import db
from routes.HomeRoute import home_bp # import do HOME
from routes.LoginRoute import login_bp, init_jwt # Import do LOGIN
from routes import GetImoveis
from routes import PostImoveisRoute
from routes import UpdateImoveisRoute
from routes import DeleteImoveisRoute
from routes.ImovelRoute import imovel_bp
from models.UserModel import User
from werkzeug.security import generate_password_hash

app = configure_app(Flask(__name__))
db.init_app(app)
init_jwt(app)#JWT está começando aqui 

with app.app_context():
    db.create_all()

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        print("Variáveis ADMIN_USERNAME e ADMIN_PASSWORD devem estar definidas para criação do 1º usuário root.")
        exit(1)

    if User.query.filter_by(username=admin_username).first():
        print(f"Usuário admin: '{admin_username}'")
    else:
        hashed_password = generate_password_hash(admin_password)
        admin = User(
            username=admin_username,
            password=hashed_password,
            roles=["ADMIN", "USUARIO", "INQUILINO", "PROPRIETARIO"]
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Usuário admin '{admin_username}' criado com sucesso.")

# Registra os blueprints
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(imovel_bp)

if __name__ == '__main__':
    app.run()
