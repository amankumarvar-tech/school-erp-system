from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Subject, Exam, Result, Homework, Timetable
from .serializers import *

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().select_related('student', 'exam', 'subject')
    serializer_class = ResultSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        student = self.request.query_params.get('student')
        exam = self.request.query_params.get('exam')
        if student: qs = qs.filter(student_id=student)
        if exam: qs = qs.filter(exam_id=exam)
        return qs

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        class_id = self.request.query_params.get('class_id')
        if class_id: qs = qs.filter(assigned_class_id=class_id)
        return qs
