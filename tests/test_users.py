from app import schemas
from jose import jwt
from app.config import settings
import pytest

# def test_root(client):
#     response = client.get("/")

#     assert response.json().get('message') == 'Hello World'
#     assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "hello123@gmail.com"
    assert response.status_code == 201

def test_login(test_user, client):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**response.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == 'bearer'
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code",  [("wrongemail@gmail.com", 'password123', 403), ("sanjeev@gmail.com", "wrongpassword", 403), ("wrongemail@gmail.com", "wrongpassword", 403), (None, "password123", 422), ("sanjeev@gmail.com", None, 422)])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})

    assert response.status_code == status_code
    # assert response.json().get("detail") == 'Invalid Credentials'