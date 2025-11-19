from flask import Flask
from config.connection import db, init_app
from controllers import authController
from controllers import userController
import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración base desde .env
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_key")   # Necesaria para sesiones
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "jwt_secret")  # Para firmar tokens JWT

    # Inicializar base de datos
    init_app(app)

    # Registrar rutas (Blueprints)
    app.register_blueprint(authController.auth_bp)
    app.register_blueprint(userController.user_bp)

    from models import users, roles

    # Crear tablas automáticamente si no existen
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
