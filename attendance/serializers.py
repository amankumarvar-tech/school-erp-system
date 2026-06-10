from rest_framework import serializers
from .models import StudentAttendance, TeacherAttendance, LeaveApplication

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = StudentAttendance
        fields = '__all__'
    def get_student_name(self, obj):
        return obj.student.full_name

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = '__all__'

class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = '__all__'
