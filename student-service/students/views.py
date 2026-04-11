from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'student_id', 'class_name']

    @action(detail=False, methods=['get'])
    def active(self, request):
        students = Student.objects.filter(is_active=True)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_class(self, request):
        class_name = request.query_params.get('class_name')
        if not class_name:
            return Response(
                {'error': 'class_name parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        students = Student.objects.filter(
            class_name=class_name,
            is_active=True
        )
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)