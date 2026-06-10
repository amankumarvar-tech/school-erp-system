from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Student, Class
from .serializers import StudentSerializer, ClassSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related('current_class')
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['admission_no', 'first_name', 'last_name', 'phone', 'email']
    ordering_fields = ['admission_no', 'first_name', 'created_at']
    
    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        class_id = self.request.query_params.get('class_id')
        if status: qs = qs.filter(status=status)
        if class_id: qs = qs.filter(current_class_id=class_id)
        return qs
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = Student.objects.count()
        active = Student.objects.filter(status='active').count()
        male = Student.objects.filter(gender='M', status='active').count()
        female = Student.objects.filter(gender='F', status='active').count()
        return Response({
            'total': total, 'active': active,
            'male': male, 'female': female,
            'inactive': total - active
        })
