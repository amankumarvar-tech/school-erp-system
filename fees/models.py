from django.db import models
from students.models import Student

class FeeStructure(models.Model):
    name = models.CharField(max_length=100)  # "Tuition Fee", "Lab Fee"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
        ('annually', 'Annually'), ('one_time', 'One Time')
    ])
    applicable_classes = models.CharField(max_length=200, blank=True)
    academic_year = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} - ₹{self.amount}"

class FeePayment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'), ('online', 'Online'), ('cheque', 'Cheque'), ('dd', 'Demand Draft')
    ]
    STATUS_CHOICES = [('paid', 'Paid'), ('pending', 'Pending'), ('partial', 'Partial'), ('overdue', 'Overdue')]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True)
    receipt_no = models.CharField(max_length=30, unique=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.CharField(max_length=200, blank=True)
    academic_year = models.CharField(max_length=10)
    month = models.CharField(max_length=20, blank=True)
    
    @property
    def balance(self):
        return float(self.amount_due) - float(self.amount_paid)
    
    def save(self, *args, **kwargs):
        if float(self.amount_paid) >= float(self.amount_due):
            self.status = 'paid'
        elif float(self.amount_paid) > 0:
            self.status = 'partial'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.receipt_no} - {self.student}"

class Expense(models.Model):
    CATEGORIES = [
        ('salary', 'Staff Salary'), ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'), ('supplies', 'Supplies'),
        ('events', 'Events'), ('other', 'Other')
    ]
    category = models.CharField(max_length=30, choices=CATEGORIES)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    approved_by = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.category} - {self.title} - ₹{self.amount}"
