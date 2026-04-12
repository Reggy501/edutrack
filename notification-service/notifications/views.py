from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['recipient_name', 'student_id', 'notification_type', 'status']

    def perform_create(self, serializer):
        serializer.save(status='pending')

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        notification = self.get_object()
        if notification.status == 'sent':
            return Response(
                {'error': 'Notification already sent'},
                status=status.HTTP_400_BAD_REQUEST
            )
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        return Response({
            'message': f'Notification sent to {notification.recipient_name}',
            'status': 'sent'
        })

    @action(detail=False, methods=['get'])
    def pending(self, request):
        notifications = Notification.objects.filter(status='pending')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        notifications = Notification.objects.filter(student_id=student_id)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_attendance_alert(self, request):
        student_id = request.data.get('student_id')
        student_name = request.data.get('student_name')
        parent_phone = request.data.get('parent_phone')
        school = request.data.get('school')
        date = request.data.get('date')

        if not all([student_id, student_name, parent_phone, date]):
            return Response(
                {'error': 'student_id, student_name, parent_phone and date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        notification = Notification.objects.create(
            recipient_name=f"Parent of {student_name}",
            recipient_phone=parent_phone,
            notification_type='attendance',
            subject=f"Attendance Alert - {student_name}",
            message=f"Dear Parent, your child {student_name} was marked absent on {date} at {school}. Please contact the school for more information.",
            student_id=student_id,
            school=school,
            status='sent',
            sent_at=timezone.now()
        )
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
