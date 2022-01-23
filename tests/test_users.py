import pytest
from app import schemas

from tests.db_fixtures import client, session


def test_root(client):
    res = client.get("/")
    assert res.json() == {"message": "i changed, a lot"}


def test_post_user(client):
    user_data = {"email": "hello1234@gmail.com", "password": "pass1234"}
    res = client.post("/users/", json=user_data)
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == user_data.get("email")
    assert res.status_code == 201
    ...
    # correct status code
    # compliance to schema
    # correct entry in db
    # existing user cant be created


def test_login_correct(client):
    user_data = {"email": "hello1234@gmail.com", "password": "pass1234"}
    auth_data = {"username": "hello1234@gmail.com", "password": "pass1234"}

    client.post("/users/", json=user_data)

    res = client.post("/login/", data=auth_data)

    assert res.status_code == 200

    login_res = schemas.Token(**res.json())

    assert login_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong@gmail.com", "password1234", 403),
        ("wrong@gmail.com", "wrongpass", 403),
        ("hello1234@gmail.com", "wrongpass", 403),
        ("hello1234@gmail.com", None, 422),
        (None, "password1234", 422),
    ],
)
def test_login_incorrect(client, email, password, status_code):
    user_data = {"email": "hello1234@gmail.com", "password": "pass1234"}
    auth_data = {"username": email, "password": password}

    client.post("/users/", json=user_data)

    res = client.post("/login/", data=auth_data)

    assert res.status_code == status_code
