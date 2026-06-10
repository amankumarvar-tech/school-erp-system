from django.db import models
from django.contrib.auth.models import User
from core.models import AcademicYear

class Class(models.Model):
    name = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    capacity = models.IntegerField(default=40)
    class_teacher = models.ForeignKey('teacher_mgmt.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10, blank=True)
    
    class Meta:
        unique_together = ['name', 'section', 'academic_year']
    
    def __str__(self):
        return f"Class {self.name} - {self.section}"

class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ]
    CATEGORY_CHOICES = [
        ('GEN', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST'), ('EWS', 'EWS')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, default='GEN')
    photo = models.ImageField(upload_to='students/', blank=True)
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    
    # Parent Info
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=15)
    father_occupation = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=15, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    
    # Academic
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    admission_date = models.DateField()
    is_active = models.BooleanField(default=True)
    previous_school = models.CharField(max_length=200, blank=True)
    
    # Medical
    medical_conditions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.admission_number} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class StudentDocument(models.Model):
    DOC_TYPES = [
        ('birth_cert', 'Birth Certificate'),
        ('aadhar', 'Aadhar Card'),
        ('transfer_cert', 'Transfer Certificate'),
        ('mark_sheet', 'Mark Sheet'),
        ('photo', 'Photograph'),
        ('other', 'Other'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    file = models.FileField(upload_to='student_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.full_name} - {self.doc_type}"
