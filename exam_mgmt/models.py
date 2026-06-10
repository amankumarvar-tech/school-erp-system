from django.db import models
from student_mgmt.models import Student, Class
from teacher_mgmt.models import Teacher
from academics_mgmt.models import Subject
from core.models import AcademicYear

class ExamType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    weightage = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Exam(models.Model):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_marks = models.IntegerField()
    pass_marks = models.IntegerField()
    venue = models.CharField(max_length=100, blank=True)
    invigilator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.exam_type.name} - {self.class_name} - {self.subject.name}"

class ExamResult(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (90-100)'),
        ('A', 'A (80-89)'),
        ('B+', 'B+ (70-79)'),
        ('B', 'B (60-69)'),
        ('C', 'C (50-59)'),
        ('D', 'D (40-49)'),
        ('E', 'E (33-39)'),
        ('F', 'F (Below 33)'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True)
    is_absent = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200, blank=True)
    entered_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    entered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['exam', 'student']
    
    def save(self, *args, **kwargs):
        if self.marks_obtained is not None and not self.is_absent:
            percentage = (self.marks_obtained / self.exam.max_marks) * 100
            if percentage >= 90: self.grade = 'A+'
            elif percentage >= 80: self.grade = 'A'
            elif percentage >= 70: self.grade = 'B+'
            elif percentage >= 60: self.grade = 'B'
            elif percentage >= 50: self.grade = 'C'
            elif percentage >= 40: self.grade = 'D'
            elif percentage >= 33: self.grade = 'E'
            else: self.grade = 'F'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.full_name} - {self.exam} - {self.marks_obtained}"

class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    total_marks = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    marks_obtained = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rank = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=3, blank=True)
    teacher_remarks = models.TextField(blank=True)
    principal_remarks = models.TextField(blank=True)
    is_promoted = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'exam_type', 'academic_year']
