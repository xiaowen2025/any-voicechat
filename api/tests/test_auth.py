import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.main import app
from api.database import Base, get_db
from api import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

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
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_request_otp():
    response = client.post("/api/auth/request-otp", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "OTP sent to your email."}

def test_verify_otp_invalid():
    response = client.post("/api/auth/verify-otp", json={"email": "test@example.com", "otp": "123456"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired OTP."}

def test_verify_otp_valid():
    # First, request an OTP
    client.post("/api/auth/request-otp", json={"email": "test2@example.com"})

    # Get the OTP from the database (for testing purposes)
    db = TestingSessionLocal()
    otp_obj = db.query(models.OTP).filter_by(email="test2@example.com").first()
    otp_code = otp_obj.otp_code
    db.close()

    # Now verify the OTP
    response = client.post("/api/auth/verify-otp", json={"email": "test2@example.com", "otp": otp_code})
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"
