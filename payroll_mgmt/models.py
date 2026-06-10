from django.db import models
from teacher_mgmt.models import Teacher
from core.models import AcademicYear

class SalaryStructure(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='salary_structure')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="House Rent Allowance")
    da = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Dearness Allowance")
    ta = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Travel Allowance")
    medical_allowance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    other_allowance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    pf_deduction = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Provident Fund")
    esi_deduction = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    other_deduction = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    effective_from = models.DateField()
    is_active = models.BooleanField(default=True)
    @property
    def gross_salary(self):
        return self.basic_salary + self.hra + self.da + self.ta + self.medical_allowance + self.other_allowance
    @property
    def total_deductions(self):
        return self.pf_deduction + self.esi_deduction + self.tax_deduction + self.other_deduction
    @property
    def net_salary(self):
        return self.gross_salary - self.total_deductions
    def __str__(self): return f"{self.teacher.full_name} - ₹{self.net_salary}"

class SalaryPayment(models.Model):
    STATUS_CHOICES = [('paid','Paid'),('pending','Pending'),('hold','On Hold')]
    PAYMENT_METHODS = [('bank','Bank Transfer'),('cash','Cash'),('cheque','Cheque')]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='salary_payments')
    month = models.IntegerField()
    year = models.IntegerField()
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.SET_NULL, null=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    advance_deduction = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    working_days = models.IntegerField(default=26)
    present_days = models.IntegerField(default=26)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='bank')
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    generated_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['teacher', 'month', 'year']
    def __str__(self): return f"{self.teacher.full_name} - {self.month}/{self.year} - ₹{self.net_salary}"

class Advance(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('approved','Approved'),('rejected','Rejected'),('repaid','Fully Repaid')]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='advances')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    applied_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    repaid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_deduction = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    def __str__(self): return f"{self.teacher.full_name} - Advance ₹{self.amount}"
