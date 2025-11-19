from flask import Flask, jsonify, render_template, g
from config.connection import db, init_app
from controllers import authController
from controllers import userController
from models.roles import Role
from models.users import User
import os
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
import time

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_key")
    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "jwt_secret")
    
    init_app(app)
    app.register_blueprint(authController.auth_bp)
    app.register_blueprint(userController.user_bp)

    # Middleware para sesiones
    @app.before_request
    def before_request():
        if hasattr(g, 'db_session'):
            g.db_session.close()

    # En app.py, agrega esta ruta temporal
    @app.route('/debug/users')
    def debug_users():
        """Ruta temporal para ver usuarios en BD"""
        try:
            from models.users import User
            users = User.query.all()
            users_data = []
            for user in users:
                users_data.append({
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'dni': user.dni,
                    'state': user.state,
                    'role_id': user.fk_role
                })
            return jsonify({
                'total_users': len(users),
                'users': users_data
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/test-db')
    def test_db():
        try:
            from sqlalchemy import text
            result = db.session.execute(text("SELECT 1"))
            db.session.close()
            return "✅ Conexión a BD exitosa"
        except Exception as e:
            return f"❌ Error de conexión: {str(e)}"
    
    @app.after_request
    def after_request(response):
        try:
            db.session.remove()
        except:
            pass
        return response

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
    def dashboard():
        return render_template('dashboard.html')

    # Crear tablas y roles por defecto al iniciar la app
    with app.app_context():
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Crear todas las tablas
                db.create_all()
                print("Tablas creadas/verificadas correctamente")
                
                # Crear roles por defecto
                Role.create_default_roles()
                print("Roles por defecto creados/verificados")
                
                break
            except OperationalError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Reintentando conexión en {wait_time} segundos...")
                    time.sleep(wait_time)
                else:
                    print(f"No se pudo conectar después de {max_retries} intentos: {e}")
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)