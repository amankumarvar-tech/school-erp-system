from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Teacher, Department
from .serializers import TeacherSerializer, DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().select_related('department')
    serializer_class = TeacherSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee_id', 'first_name', 'last_name', 'phone', 'subjects']
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response({
            'total': Teacher.objects.count(),
            'active': Teacher.objects.filter(status='active').count(),
            'on_leave': Teacher.objects.filter(status='on_leave').count(),
        })
