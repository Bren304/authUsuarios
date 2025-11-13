from flask import Blueprint, request, jsonify
from config.connection import db
from models import users
import jwt
import datetime
import os

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# ✅ Registro de usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Verificar si ya existe un usuario con el mismo email o username
    if users.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email ya registrado"}), 400

    if users.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username ya en uso"}), 400

    # Crear nuevo usuario
    user = users(
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


# Login de usuario (genera JWT)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.query.filter_by(email=data['email']).first()

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
