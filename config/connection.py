import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool

load_dotenv()

db = SQLAlchemy()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def init_app(app):
    # OPCIÓN 1: NullPool (RECOMENDADO para Clever Cloud con 5 conexiones)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        'poolclass': NullPool,  # Sin pool - conexión por request
    }
    
    db.init_app(app)
    
    print("Configuración de BD: NullPool (sin conexiones persistentes)")