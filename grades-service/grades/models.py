from django.db import models

class Grade(models.Model):
    TERM_CHOICES = [
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    ]

    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=200)
    class_name = models.CharField(max_length=50)
    school = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    year = models.IntegerField()
    recorded_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.subject} - {self.term} {self.year}"

    @property
    def percentage(self):
        return round((self.score / self.max_score) * 100, 2)

    @property
    def grade_letter(self):
        p = self.percentage
        if p >= 75: return 'A'
        elif p >= 65: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else: return 'F'

    class Meta:
        ordering = ['-year', 'term', 'student_id']
        unique_together = ['student_id', 'subject', 'term', 'year']
