import os 

def configure_app(app):
    app.config['HOST'] = os.getenv("FLASK_HOST")
    app.config['PORT'] = os.getenv("FLASK_RUN_PORT")
    if os.getenv("FLASK_ENV") == "development":
        app.config['DEBUG'] = True
    else:
        app.config['DEBUG'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    return app
