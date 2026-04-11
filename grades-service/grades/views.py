from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Grade
from .serializers import GradeSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['student_id', 'student_name', 'subject', 'class_name']

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        grades = Grade.objects.filter(student_id=student_id)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def report_card(self, request):
        student_id = request.query_params.get('student_id')
        term = request.query_params.get('term')
        year = request.query_params.get('year')
        if not all([student_id, term, year]):
            return Response(
                {'error': 'student_id, term and year are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        grades = Grade.objects.filter(
            student_id=student_id,
            term=term,
            year=year
        )
        serializer = self.get_serializer(grades, many=True)
        average = grades.aggregate(avg=Avg('score'))['avg']
        return Response({
            'student_id': student_id,
            'term': term,
            'year': year,
            'grades': serializer.data,
            'average_score': round(average, 2) if average else 0
        })
