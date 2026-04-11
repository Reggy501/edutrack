from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'student_name', 'class_name', 'date', 'status', 'recorded_by']
    search_fields = ['student_id', 'student_name', 'class_name']
    list_filter = ['status', 'class_name', 'date']