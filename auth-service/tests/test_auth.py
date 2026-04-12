import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from authentication.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_user(db):
    return User.objects.create_user(
        username='teacher1',
        email='teacher1@school.com',
        password='securepass123',
        role='teacher',
        school='Dar es Salaam Secondary School'
    )

@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('register')
    data = {
        'username': 'newteacher',
        'email': 'newteacher@school.com',
        'password': 'securepass123',
        'first_name': 'John',
        'last_name': 'Doe',
        'role': 'teacher',
        'school': 'Dar es Salaam Secondary School'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_login_user(api_client, sample_user):
    url = reverse('login')
    data = {
        'username': 'teacher1',
        'password': 'securepass123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_login_wrong_password(api_client, sample_user):
    url = reverse('login')
    data = {
        'username': 'teacher1',
        'password': 'wrongpassword'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_get_profile(api_client, sample_user):
    api_client.force_authenticate(user=sample_user)
    url = reverse('profile')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == 'teacher1'
    assert response.data['role'] == 'teacher'

@pytest.mark.django_db
def test_profile_requires_auth(api_client):
    url = reverse('profile')
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_register_duplicate_username(api_client, sample_user):
    url = reverse('register')
    data = {
        'username': 'teacher1',
        'email': 'another@school.com',
        'password': 'securepass123',
        'role': 'teacher'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400
