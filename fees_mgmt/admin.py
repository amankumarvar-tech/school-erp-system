from django.contrib import admin
from .models import FeeStructure, FeePayment, Scholarship
@admin.register(FeePayment)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_structure', 'amount_due', 'amount_paid', 'status', 'due_date']
    list_filter = ['status', 'payment_method']
admin.site.register(FeeStructure)
admin.site.register(Scholarship)
