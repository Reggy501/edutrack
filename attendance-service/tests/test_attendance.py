import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from attendance.models import Attendance

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_attendance(db):
    return Attendance.objects.create(
        student_id='STU001',
        student_name='John Doe',
        class_name='Form 1',
        school='Dar es Salaam Secondary School',
        date='2026-01-15',
        status='present',
        recorded_by='Teacher James'
    )

@pytest.mark.django_db
def test_create_attendance(api_client):
    url = reverse('attendance-list')
    data = {
        'student_id': 'STU002',
        'student_name': 'Jane Smith',
        'class_name': 'Form 2',
        'school': 'Dar es Salaam Secondary School',
        'date': '2026-01-15',
        'status': 'present',
        'recorded_by': 'Teacher James'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['status'] == 'present'

@pytest.mark.django_db
def test_get_all_attendance(api_client, sample_attendance):
    url = reverse('attendance-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_by_student(api_client, sample_attendance):
    url = reverse('attendance-by-student') + '?student_id=STU001'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_by_date(api_client, sample_attendance):
    url = reverse('attendance-by-date') + '?date=2026-01-15'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_mark_absent(api_client):
    url = reverse('attendance-list')
    data = {
        'student_id': 'STU003',
        'student_name': 'Peter Paul',
        'class_name': 'Form 1',
        'school': 'Dar es Salaam Secondary School',
        'date': '2026-01-16',
        'status': 'absent',
        'recorded_by': 'Teacher James'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['status'] == 'absent'

@pytest.mark.django_db
def test_attendance_summary(api_client, sample_attendance):
    url = reverse('attendance-summary') + '?student_id=STU001'
    response = api_client.get(url)
    assert response.status_code == 200
