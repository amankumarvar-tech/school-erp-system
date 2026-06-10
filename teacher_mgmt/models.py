from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_dept')
    
    def __str__(self):
        return self.name

class Teacher(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    EMPLOYMENT_CHOICES = [
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('part_time', 'Part Time'),
        ('guest', 'Guest Faculty'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='teachers/', blank=True)
    
    # Contact
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15, blank=True)
    
    # Professional
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    joining_date = models.DateField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default='permanent')
    
    # Salary
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey('academics_mgmt.Subject', on_delete=models.CASCADE)
    class_assigned = models.ForeignKey('student_mgmt.Class', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['teacher', 'subject', 'class_assigned']
    
    def __str__(self):
        return f"{self.teacher.full_name} - {self.subject.name} - {self.class_assigned}"

class TeacherLeave(models.Model):
    LEAVE_TYPES = [
        ('casual', 'Casual Leave'),
        ('sick', 'Sick Leave'),
        ('earned', 'Earned Leave'),
        ('maternity', 'Maternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.teacher.full_name} - {self.leave_type} ({self.from_date})"
