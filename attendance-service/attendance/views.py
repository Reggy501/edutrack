from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['student_id', 'student_name', 'class_name', 'date']

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        records = Attendance.objects.filter(student_id=student_id)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response(
                {'error': 'date parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        records = Attendance.objects.filter(date=date)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        summary = Attendance.objects.filter(
            student_id=student_id
        ).values('status').annotate(count=Count('status'))
        return Response(summary)