from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import StudentAttendance, TeacherAttendance, LeaveApplication
from .serializers import *

class StudentAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StudentAttendance.objects.all().select_related('student')
    serializer_class = StudentAttendanceSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        date = self.request.query_params.get('date')
        student = self.request.query_params.get('student')
        if date: qs = qs.filter(date=date)
        if student: qs = qs.filter(student_id=student)
        return qs
    
    @action(detail=False, methods=['get'])
    def today_summary(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        records = StudentAttendance.objects.filter(date=today)
        return Response({
            'date': str(today),
            'present': records.filter(status='present').count(),
            'absent': records.filter(status='absent').count(),
            'late': records.filter(status='late').count(),
            'total': records.count()
        })

class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer

class LeaveApplicationViewSet(viewsets.ModelViewSet):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
