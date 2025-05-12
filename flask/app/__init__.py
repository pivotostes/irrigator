from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.sensores import sensores_bp
    from .routes.bombas import bombas_bp

    app.register_blueprint(sensores_bp)
    app.register_blueprint(bombas_bp)

    return app
