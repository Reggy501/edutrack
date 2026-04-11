import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from grades.models import Grade

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_grade(db):
    return Grade.objects.create(
        student_id='STU001',
        student_name='John Doe',
        class_name='Form 1',
        school='Dar es Salaam Secondary School',
        subject='Mathematics',
        score=85,
        max_score=100,
        term='Term 1',
        year=2026,
        recorded_by='Teacher James'
    )

@pytest.mark.django_db
def test_create_grade(api_client):
    url = reverse('grade-list')
    data = {
        'student_id': 'STU002',
        'student_name': 'Jane Smith',
        'class_name': 'Form 2',
        'school': 'Dar es Salaam Secondary School',
        'subject': 'English',
        'score': 78,
        'max_score': 100,
        'term': 'Term 1',
        'year': 2026,
        'recorded_by': 'Teacher Mary'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['subject'] == 'English'

@pytest.mark.django_db
def test_get_all_grades(api_client, sample_grade):
    url = reverse('grade-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_grade_percentage(api_client, sample_grade):
    url = reverse('grade-detail', args=[sample_grade.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['percentage'] == 85.0

@pytest.mark.django_db
def test_grade_letter(api_client, sample_grade):
    url = reverse('grade-detail', args=[sample_grade.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['grade_letter'] == 'A'

@pytest.mark.django_db
def test_get_by_student(api_client, sample_grade):
    url = reverse('grade-by-student') + '?student_id=STU001'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_report_card(api_client, sample_grade):
    url = reverse('grade-report-card') + '?student_id=STU001&term=Term 1&year=2026'
    response = api_client.get(url)
    assert response.status_code == 200
    assert 'grades' in response.data
    assert 'average_score' in response.data
