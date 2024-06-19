# tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Create a test database URL for MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/flask_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Setup: create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: drop database tables
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    response = client.post("/api/users/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_user_existing_username():
    # Create a user
    client.post("/api/users/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    # Try to create a user with the same username
    response = client.post("/api/users/", json={"username": "testuser", "email": "test2@example.com", "password": "password2"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_read_user():
    # Create a user
    response = client.post("/api/users/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    user_id = response.json()["id"]
    # Retrieve the user by ID
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_read_user_not_found():
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
