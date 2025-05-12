from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    from .routes.main import main_bp
    from .routes.sensores import sensores_bp
    from .routes.bombas import bombas_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(sensores_bp)
    app.register_blueprint(bombas_bp)

    return app
