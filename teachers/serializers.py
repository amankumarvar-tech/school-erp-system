from rest_framework import serializers
from .models import Teacher, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = Teacher
        fields = '__all__'
    def get_department_name(self, obj):
        return obj.department.name if obj.department else None
