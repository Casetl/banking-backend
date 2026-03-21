import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()

    url = "/api/v1/auth/register/"
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "12345678"
    }

    response = client.post(url, data)

    assert response.status_code == 201
    assert User.objects.filter(email="test@example.com").exists()
    
@pytest.mark.django_db
def test_user_login():
    client = APIClient()

    User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="12345678"
    )

    url = "/api/v1/auth/login/"
    data = {
        "email": "test@example.com",
        "password": "12345678"
    }

    response = client.post(url, data)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_me_endpoint():
    client = APIClient()

    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="12345678"
    )

    login = client.post("/api/v1/auth/login/", {
        "email": "test@example.com",
        "password": "12345678"
    })

    token = login.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get("/api/v1/auth/me/")

    assert response.status_code == 200
    assert response.data["email"] == "test@example.com"
    
@pytest.mark.django_db
def test_get_profile():
    client = APIClient()

    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="12345678"
    )

    login = client.post("/api/v1/auth/login/", {
        "email": "test@example.com",
        "password": "12345678"
    })

    token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get("/api/v1/auth/me/profile/")

    assert response.status_code == 200
    assert "full_name" in response.data
    
@pytest.mark.django_db
def test_update_profile():
    client = APIClient()

    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="12345678"
    )

    login = client.post("/api/v1/auth/login/", {
        "email": "test@example.com",
        "password": "12345678"
    })

    token = login.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {
        "full_name": "Juan Perez",
        "phone": "123456789",
        "address": "Test address"
    }

    response = client.put("/api/v1/auth/me/profile/", data)

    assert response.status_code == 200
    assert response.data["full_name"] == "Juan Perez"