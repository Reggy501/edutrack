from django.db import models

class Notification(models.Model):
    TYPE_CHOICES = [
        ('attendance', 'Attendance Alert'),
        ('grade', 'Grade Report'),
        ('announcement', 'Announcement'),
        ('reminder', 'Reminder'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    recipient_name = models.CharField(max_length=200)
    recipient_phone = models.CharField(max_length=20, blank=True, null=True)
    recipient_email = models.CharField(max_length=200, blank=True, null=True)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    student_id = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.notification_type} - {self.recipient_name} - {self.status}"

    class Meta:
        ordering = ['-created_at']
