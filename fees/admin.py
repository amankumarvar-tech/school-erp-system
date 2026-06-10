from django.contrib import admin
from .models import FeeStructure, FeePayment, Expense

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_no', 'student', 'amount_due', 'amount_paid', 'status']
    list_filter = ['status']

admin.site.register(FeeStructure)
admin.site.register(Expense)
