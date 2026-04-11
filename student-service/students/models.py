from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    class_name = models.CharField(max_length=50)
    school = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=20)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id}"

    class Meta:
        ordering = ['last_name', 'first_name']