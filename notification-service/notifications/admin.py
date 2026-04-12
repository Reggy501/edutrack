from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient_name', 'notification_type', 'subject', 'status', 'created_at']
    list_filter = ['notification_type', 'status']
    search_fields = ['recipient_name', 'student_id', 'subject']
