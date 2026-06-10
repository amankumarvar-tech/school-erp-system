from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import FeeStructure, FeePayment, Expense
from .serializers import *

class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer

class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all().select_related('student')
    serializer_class = FeePaymentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['receipt_no', 'student__first_name', 'student__last_name', 'student__admission_no']
    
    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        student = self.request.query_params.get('student')
        if status: qs = qs.filter(status=status)
        if student: qs = qs.filter(student_id=student)
        return qs
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_due = FeePayment.objects.aggregate(t=Sum('amount_due'))['t'] or 0
        total_collected = FeePayment.objects.aggregate(t=Sum('amount_paid'))['t'] or 0
        pending = FeePayment.objects.filter(status='pending').count()
        overdue = FeePayment.objects.filter(status='overdue').count()
        return Response({
            'total_due': float(total_due),
            'total_collected': float(total_collected),
            'pending_count': pending,
            'overdue_count': overdue,
            'collection_rate': round((float(total_collected)/float(total_due)*100) if total_due else 0, 2)
        })

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        from django.db.models import Sum
        total = Expense.objects.aggregate(t=Sum('amount'))['t'] or 0
        by_category = list(Expense.objects.values('category').annotate(total=Sum('amount')))
        return Response({'total': float(total), 'by_category': by_category})
