import pytest
import json
from app import create_app
from config.connection import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register_user(client):
    """Test registro de usuario"""
    user_data = {
        "dni": "12345678",
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "phone": "123456789"
    }
    
    response = client.post('/auth/register', 
                         data=json.dumps(user_data),
                         content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "message" in data

def test_login_user(client):
    """Test login de usuario"""
    # Primero registrar un usuario
    user_data = {
        "dni": "12345678",
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    client.post('/auth/register', 
               data=json.dumps(user_data),
               content_type='application/json')
    
    # Luego hacer login
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = client.post('/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "token" in data
    assert "user" in data