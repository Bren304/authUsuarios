from flask import Blueprint, request, jsonify
from config.connection import db
from middleware.authMiddleware import token_required
from models.users import User
import jwt
import datetime
import os

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# ✅ Registro de usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email ya registrado"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username ya en uso"}), 400
    
    user = User(
        dni=data['dni'],
        username=data['username'],
        email=data['email'],
        phone=data.get('phone'),
        fk_role=data.get('role', 1)   # rol por defecto 1 (usuario)
    )
    user.set_password(data['password'])  # hash seguro

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente"}), 201


# ✅ Login de usuario
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    }, os.getenv("JWT_SECRET"), algorithm="HS256")

    return jsonify({
        "message": "Login exitoso",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.name if user.role else None
        }
    }), 200

# En authController.py
@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():    
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200