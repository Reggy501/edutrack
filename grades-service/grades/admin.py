from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'student_name', 'subject', 'score', 'term', 'year', 'recorded_by']
    search_fields = ['student_id', 'student_name', 'subject']
    list_filter = ['term', 'year', 'class_name']
