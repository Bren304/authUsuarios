from config.connection import db
from sqlalchemy.orm import relationship
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), unique = True, nullable=True)
    state = db.Column(db.Boolean, default=True, nullable=False)

    # Relación con la tabla Roles
    fk_role = db.Column(db.Integer, ForeignKey('roles.id'), nullable=False, default='1')

    role = relationship('Role', back_populates='users')

    # Genera el hash de la contraseña
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    # Verifica la contraseña
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        """Representación del objeto para depuración."""
        return f"<User {self.username} ({self.email})>"

