from flask import Flask, render_template
from config.connection import db, init_app
from controllers import authController
from controllers import userController
import os
from dotenv import load_dotenv

from middleware.authMiddleware import token_required

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_key")
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "jwt_secret")
    
    # Configuración del pool de conexiones
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        'pool_size': 2,
        'max_overflow': 1,
        'pool_recycle': 180,
        'pool_pre_ping': True,
        'pool_timeout': 15
    }
    
    init_app(app)
    app.register_blueprint(authController.auth_bp)
    app.register_blueprint(userController.user_bp)
    
    from models.users import User
    from models.roles import Role
    
    # Rutas para las vistas HTML
    @app.route('/')
    def index():
        return render_template('login.html')
    
    @app.route('/login')
    def show_login():
        return render_template('login.html')
    
    @app.route('/register')
    def show_register():
        return render_template('register.html')
    
    @app.route('/dashboard')
    @token_required
    def dashboard():
        return render_template('dashboard.html')
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)