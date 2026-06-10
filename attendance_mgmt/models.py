from django.db import models
from student_mgmt.models import Student, Class
from teacher_mgmt.models import Teacher
from academics_mgmt.models import Subject

class StudentAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'On Leave'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=200, blank=True)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"

class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('on_leave', 'On Leave'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['teacher', 'date']
    
    def __str__(self):
        return f"{self.teacher.full_name} - {self.date} - {self.status}"
