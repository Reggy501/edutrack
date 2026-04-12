import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from notifications.models import Notification

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_notification(db):
    return Notification.objects.create(
        recipient_name='Parent of John Doe',
        recipient_phone='+255712345678',
        notification_type='attendance',
        subject='Attendance Alert',
        message='Your child was absent today',
        student_id='STU001',
        school='Dar es Salaam Secondary School',
        status='pending'
    )

@pytest.mark.django_db
def test_create_notification(api_client):
    url = reverse('notification-list')
    data = {
        'recipient_name': 'Parent of Jane Smith',
        'recipient_phone': '+255787654321',
        'notification_type': 'grade',
        'subject': 'Grade Report - Term 1',
        'message': 'Your child scored 85% in Mathematics',
        'student_id': 'STU002',
        'school': 'Dar es Salaam Secondary School',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['status'] == 'pending'

@pytest.mark.django_db
def test_get_all_notifications(api_client, sample_notification):
    url = reverse('notification-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_send_notification(api_client, sample_notification):
    url = reverse('notification-send', args=[sample_notification.id])
    response = api_client.post(url)
    assert response.status_code == 200
    assert response.data['status'] == 'sent'

@pytest.mark.django_db
def test_get_pending_notifications(api_client, sample_notification):
    url = reverse('notification-pending')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_by_student(api_client, sample_notification):
    url = reverse('notification-by-student') + '?student_id=STU001'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_send_attendance_alert(api_client):
    url = reverse('notification-send-attendance-alert')
    data = {
        'student_id': 'STU001',
        'student_name': 'John Doe',
        'parent_phone': '+255712345678',
        'school': 'Dar es Salaam Secondary School',
        'date': '2026-04-11'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['status'] == 'sent'
