import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash
from bson import ObjectId
from datetime import datetime
from mongoengine import connect, disconnect
import mongomock

# เพิ่ม path เพื่อให้ import app ได้ถูกต้อง
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import User

@pytest.fixture(autouse=True)
def mongo_mock():
    """
    Fixture for mocking the MongoDB connection.
    This ensures that tests run against a mock database, not the real one.
    """
    disconnect()
    mock_client = mongomock.MongoClient(uuidRepresentation="standard")
    connect(
        db='testdb',
        alias='default',
        host='mongodb://localhost',
        mongo_client_class=lambda *args, **kwargs: mock_client
    )
    yield
    disconnect()

@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.
    This allows us to make requests to the app's endpoints.
    """
    with app.test_client() as client:
        yield client

def test_register_success(client):
    response = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    # 🔹 แก้ไข assertion ให้ตรงกับผลลัพธ์ที่ API คืนค่า
    assert response.status_code == 200
    assert response.get_json()["msg"] == "User registered successfully"

def test_register_duplicate(client):
    User(username="testuser", password="hashed").save()
    response = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 400
    
    assert response.get_json()["msg"] == "Username already exists"

def test_login_success(client):
    """
    Test a successful user login.
    - Creates a user with a hashed password in the mock database.
    - Sends a POST request to '/api/login' with the correct credentials.
    - Asserts a 200 OK status code and that an access token is returned.
    """
    hashed_pw = generate_password_hash("testpass")
    User(username="testuser", password=hashed_pw).save()
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["username"] == "testuser"

def test_login_invalid_password(client):
    """
    Test login with an incorrect password.
    - Creates a user in the mock database.
    - Sends a POST request to '/api/login' with a wrong password.
    - Asserts a 401 Unauthorized status code and the invalid credentials message.
    """
    hashed_pw = generate_password_hash("correctpass")
    User(username="testuser", password=hashed_pw).save()
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Invalid credentials"

def test_login_nonexistent_user(client):
    """
    Test login with a username that does not exist.
    - Sends a POST request with a username that isn't in the database.
    - Asserts a 401 Unauthorized status code and the invalid credentials message.
    """
    response = client.post('/api/login', json={
        "username": "nonexistentuser",
        "password": "somepass"
    })
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Invalid credentials"

def test_login_missing_fields(client):
    """
    Test login with missing required fields in the request body.
    - Sends a POST request with an incomplete payload.
    - Asserts a 400 Bad Request status code.
    """
    response = client.post('/api/login', json={"username": "testuser"})
    assert response.status_code == 400
