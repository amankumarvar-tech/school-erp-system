from django.db import models
from students.models import Student, Class
from teachers.models import Teacher

class StudentAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'), ('absent', 'Absent'),
        ('late', 'Late'), ('half_day', 'Half Day'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=200, blank=True)
    marked_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ['student', 'date']
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'), ('absent', 'Absent'),
        ('late', 'Late'), ('on_leave', 'On Leave'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['teacher', 'date']
    
    def __str__(self):
        return f"{self.teacher} - {self.date} - {self.status}"

class LeaveApplication(models.Model):
    LEAVE_TYPES = [
        ('sick', 'Sick Leave'), ('casual', 'Casual Leave'),
        ('emergency', 'Emergency'), ('other', 'Other')
    ]
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Leave - {self.from_date} to {self.to_date}"
