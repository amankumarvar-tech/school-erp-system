from django.db import models
from django.utils import timezone

class Class(models.Model):
    name = models.CharField(max_length=20)  # e.g. "10-A", "12-B"
    grade = models.IntegerField()  # 1-12
    section = models.CharField(max_length=5)
    capacity = models.IntegerField(default=40)
    class_teacher = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Class {self.grade}-{self.section}"
    
    class Meta:
        unique_together = ['grade', 'section']

class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('graduated', 'Graduated'), ('transferred', 'Transferred')]
    
    admission_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    roll_number = models.IntegerField()
    admission_date = models.DateField(default=timezone.now)
    
    # Contact
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Parent Info
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=15, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    mother_phone = models.CharField(max_length=15, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.admission_no} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
