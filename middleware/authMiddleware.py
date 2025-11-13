import jwt
from flask import request, jsonify
from functools import wraps
from models import users
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Extrae el token del header "Authorization: Bearer <token>"
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token no enviado"}), 401
        
        try:
            decoded = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            user = users.query.get(decoded["id"])

            if not user:
                return jsonify({"error": "Usuario no encontrado"}), 404
            
            request.user = user  # Inyecta el user en la request

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token ha expirado"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated