from flask import Blueprint, request, jsonify
from config.connection import db
from middleware.authMiddleware import token_required
from models.users import User
import jwt
import datetime
import os
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"📨 Datos recibidos: {data}") # Debug

        # Verificar si ya existe
        existing_email = User.query.filter_by(email=data['email']).first()
        existing_username = User.query.filter_by(username=data['username']).first()
        existing_dni = User.query.filter_by(dni=data['dni']).first()
        
        if existing_email:
            db.session.close()
            print("Email ya existe")  # Debug
            return jsonify({"error": "Email ya registrado"}), 400

        if existing_username:
            db.session.close()
            print("Username ya existe")  # Debug
            return jsonify({"error": "Username ya en uso"}), 400

        if existing_dni:
            db.session.close()
            print("DNI ya existe")  # Debug
            return jsonify({"error": "DNI ya registrado"}), 400

        # Crear usuario
        user = User(
            dni=data['dni'],
            username=data['username'],
            email=data['email'],
            phone=data.get('phone'),
            fk_role=data.get('role', 1)
        )
        user.set_password(data['password'])
        
        print(f"Usuario a crear: {user}")  # Debug

        db.session.add(user)
        db.session.commit()
        
        print("Usuario creado exitosamente")  # Debug
        response = jsonify({"message": "Usuario registrado correctamente"}), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR en registro: {str(e)}")  # Debug detallado
        print(f"Tipo de error: {type(e)}")  # Debug
        response = jsonify({"error": f"Error al crear usuario: {str(e)}"}), 500
    finally:
        db.session.close()
    
    return response
    try:
        data = request.get_json()

        # Verificar si ya existe
        existing_email = User.query.filter_by(email=data['email']).first()
        existing_username = User.query.filter_by(username=data['username']).first()
        
        if existing_email:
            db.session.close()  # ✅ Cerrar sesión
            return jsonify({"error": "Email ya registrado"}), 400

        if existing_username:
            db.session.close()  # ✅ Cerrar sesión
            return jsonify({"error": "Username ya en uso"}), 400

        # Crear usuario
        user = User(
            dni=data['dni'],
            username=data['username'],
            email=data['email'],
            phone=data.get('phone'),
            fk_role=data.get('role', 1)
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()
        
        response = jsonify({"message": "Usuario registrado correctamente"}), 201
        
    except Exception as e:
        db.session.rollback()
        response = jsonify({"error": "Error al crear usuario"}), 500
    finally:
        db.session.close()  # ✅ CERRAR SESIÓN SIEMPRE
    
    return response

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            db.session.close()  # Cerrar sesión
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Verificar si el usuario está activo
        if not user.state:
            db.session.close()  # Cerrar sesión
            return jsonify({"error": "Usuario desactivado"}), 401

        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        }, os.getenv("JWT_SECRET"), algorithm="HS256")

        response = jsonify({
            "message": "Login exitoso",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.name if user.role else None,
                "dni": user.dni,
                "phone": user.phone
            }
        }), 200
        
    except Exception as e:
            print(f"ERROR DETALLADO en login: {str(e)}")  # Debug detallado
            print(f"Tipo de error: {type(e).__name__}")  # Debug
            import traceback
            print(f"Traceback completo: {traceback.format_exc()}")  # Debug completo
            response = jsonify({"error": "Error en el servidor"}), 500
    finally:
        db.session.close()  # CERRAR SESIÓN SIEMPRE
    
    return response

@auth_bp.route('/verify-token', methods=['POST'])
@token_required
def verify_token():
    """Verificar si el token es válido"""
    try:
        # Si llegamos aquí, el token es válido (pasó el middleware)
        user = getattr(request, 'user', None)
        if user:
            return jsonify({
                "valid": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role.name if user.role else None
                }
            }), 200
        else:
            return jsonify({"valid": False, "error": "Usuario no encontrado"}), 401
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 401

# Función helper para obtener el usuario del token
def get_current_user():
    return getattr(request, 'user', None)