from rest_framework import serializers
from .models import Subject, Exam, Result, Homework, Timetable

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    percentage = serializers.ReadOnlyField()
    student_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    class Meta:
        model = Result
        fields = '__all__'
    def get_student_name(self, obj):
        return obj.student.full_name
    def get_subject_name(self, obj):
        return obj.subject.name

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'
