import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

load_dotenv()

db = SQLAlchemy()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# En tu connection.py, asegúrate de cerrar conexiones correctamente
def init_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        'pool_size': 2,
        'max_overflow': 1,
        'pool_recycle': 180,  # 3 minutos
        'pool_pre_ping': True,
        'pool_timeout': 15
    }
    db.init_app(app)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()