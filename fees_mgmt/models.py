from django.db import models
from student_mgmt.models import Student, Class
from core.models import AcademicYear

class FeeStructure(models.Model):
    FEE_TYPES = [
        ('tuition', 'Tuition Fee'),
        ('transport', 'Transport Fee'),
        ('library', 'Library Fee'),
        ('sports', 'Sports Fee'),
        ('lab', 'Lab Fee'),
        ('exam', 'Exam Fee'),
        ('uniform', 'Uniform Fee'),
        ('misc', 'Miscellaneous'),
    ]
    FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half Yearly'),
        ('annually', 'Annually'),
        ('one_time', 'One Time'),
    ]
    
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='fee_structure')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    due_date = models.IntegerField(default=10, help_text="Day of month when fee is due")
    late_fine = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.class_name} - {self.fee_type} - {self.amount}"

class FeePayment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online Transfer'),
        ('upi', 'UPI'),
        ('dd', 'Demand Draft'),
    ]
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('overdue', 'Overdue'),
        ('waived', 'Waived'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    remarks = models.CharField(max_length=200, blank=True)
    collected_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.full_name} - {self.fee_structure.fee_type} - {self.status}"
    
    @property
    def balance(self):
        return self.amount_due + self.fine_amount - self.discount - self.amount_paid

class Scholarship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scholarships')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    reason = models.TextField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student.full_name} - {self.name}"
