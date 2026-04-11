from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    percentage = serializers.ReadOnlyField()
    grade_letter = serializers.ReadOnlyField()

    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
