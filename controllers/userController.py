from flask import Blueprint, request, jsonify
from config.connection import db
from models.users import User
from middleware.authMiddleware import token_required

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')


# Obtener todos los usuarios
@token_required
@user_bp.route('/', methods=['GET'])
def get_users():
    # ✅ Cambiar 'users' por 'all_users' para evitar conflicto
    all_users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "dni": u.dni,
            "username": u.username,
            "email": u.email,
            "phone": u.phone,
            "state": u.state,
            "role": u.role.name if u.role else None,
            "created_at": u.created_at.isoformat() if u.created_at else None
        }
        for u in all_users
    ]), 200


# Obtener un usuario por ID
@token_required
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "dni": user.dni,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "state": user.state,
        "role": user.role.name if user.role else None,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200


# Crear usuario (similar al registro, pero desde admin)
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El correo ya está registrado"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "El username ya está en uso"}), 400

    user = User(
        dni=data["dni"],
        username=data["username"],
        email=data["email"],
        phone=data.get("phone"),
        fk_role=data.get("role", 1),  # rol por defecto: user
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario creado correctamente"}), 201


# Editar usuario
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)  # ✅ Usar 'User' en lugar de 'users'
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()

    user.username = data.get("username", user.username)
    user.phone = data.get("phone", user.phone)
    user.fk_role = data.get("role", user.fk_role)

    db.session.commit()

    return jsonify({"message": "Usuario actualizado correctamente"}), 200


# Cambiar estado (activar / desactivar)
@user_bp.route('/<int:user_id>/state', methods=['PATCH'])
def change_state(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    user.state = not user.state  # alterna true/false
    db.session.commit()

    return jsonify({"message": f"Usuario {'activado' if user.state else 'desactivado'}"}), 200


# Eliminar usuario
@token_required
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado correctamente"}), 200