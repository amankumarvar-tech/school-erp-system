from rest_framework import serializers
from .models import FeeStructure, FeePayment, Expense

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class FeePaymentSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = FeePayment
        fields = '__all__'
    def get_student_name(self, obj):
        return obj.student.full_name

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
