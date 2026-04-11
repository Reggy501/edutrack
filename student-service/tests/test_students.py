import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from students.models import Student

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_student(db):
    return Student.objects.create(
        first_name='John',
        last_name='Doe',
        student_id='STU001',
        date_of_birth='2010-01-15',
        gender='Male',
        class_name='Form 1',
        school='Dar es Salaam Secondary School',
        parent_phone='+255712345678',
        is_active=True
    )

@pytest.mark.django_db
def test_create_student(api_client):
    url = reverse('student-list')
    data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'student_id': 'STU002',
        'date_of_birth': '2011-03-20',
        'gender': 'Female',
        'class_name': 'Form 2',
        'school': 'Dar es Salaam Secondary School',
        'parent_phone': '+255787654321',
        'is_active': True
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['first_name'] == 'Jane'

@pytest.mark.django_db
def test_get_all_students(api_client, sample_student):
    url = reverse('student-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_active_students(api_client, sample_student):
    url = reverse('student-active')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_search_student(api_client, sample_student):
    url = reverse('student-list') + '?search=John'
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]['first_name'] == 'John'

@pytest.mark.django_db
def test_deactivate_student(api_client, sample_student):
    url = reverse('student-detail', args=[sample_student.id])
    response = api_client.patch(url, {'is_active': False}, format='json')
    assert response.status_code == 200
    assert response.data['is_active'] == False

@pytest.mark.django_db
def test_get_by_class(api_client, sample_student):
    url = reverse('student-by-class') + '?class_name=Form 1'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
