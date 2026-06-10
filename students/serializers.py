from rest_framework import serializers
from .models import Student, Class

class ClassSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    class Meta:
        model = Class
        fields = '__all__'
    def get_student_count(self, obj):
        return Student.objects.filter(current_class=obj, status='active').count()

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class_name = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'
    def get_class_name(self, obj):
        return str(obj.current_class) if obj.current_class else None
