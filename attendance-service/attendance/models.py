from django.db import models

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=200)
    class_name = models.CharField(max_length=50)
    school = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.date} - {self.status}"

    class Meta:
        ordering = ['-date', 'student_id']
        unique_together = ['student_id', 'date']