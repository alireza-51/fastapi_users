import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from app.auth import create_access_token
from app.models import User
from dotenv import load_dotenv

load_dotenv()

# Setup synchronous database engine for testing
SQLALCHEMY_DATABASE_URL = os.getenv('TEST_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the synchronous test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def db_session():
    # This fixture sets up a session for the test cases
    with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="module")
def client():
    # This fixture sets up the TestClient for testing
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user(db_session):
    # Create and return a test user
    user = User(username="testuser", password="hashedpassword", role="user", email='user@example.com')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def admin_user(db_session):
    # Create and return an admin user
    user = User(username="admin", password="hashedpassword", role="admin", email='admin@example.com')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_token(test_user):
    # Create and return an authentication token
    token = create_access_token(data={"sub": test_user.username})
    return {"token": token, "user": test_user}

@pytest.fixture
def admin_token(admin_user):
    # Create and return an admin authentication token
    token = create_access_token(data={"sub": admin_user.username})
    return {"token": token, "user": admin_user}