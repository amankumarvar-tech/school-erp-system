from django.db import models
from students.models import Student, Class
from teachers.models import Teacher

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    classes = models.ManyToManyField(Class, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    max_marks = models.IntegerField(default=100)
    passing_marks = models.IntegerField(default=33)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Exam(models.Model):
    EXAM_TYPES = [
        ('unit_test', 'Unit Test'), ('mid_term', 'Mid Term'),
        ('final', 'Final Exam'), ('practical', 'Practical'),
    ]
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    academic_year = models.CharField(max_length=10)  # e.g. "2024-25"
    classes = models.ManyToManyField(Class, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.academic_year})"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.IntegerField(default=100)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['student', 'exam', 'subject']
    
    @property
    def percentage(self):
        return round((float(self.marks_obtained) / self.max_marks) * 100, 2)
    
    def save(self, *args, **kwargs):
        pct = self.percentage
        if pct >= 90: self.grade = 'A+'
        elif pct >= 80: self.grade = 'A'
        elif pct >= 70: self.grade = 'B+'
        elif pct >= 60: self.grade = 'B'
        elif pct >= 50: self.grade = 'C'
        elif pct >= 33: self.grade = 'D'
        else: self.grade = 'F'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks_obtained}"

class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    def __str__(self):
        return f"{self.title} - {self.assigned_class}"

class Timetable(models.Model):
    DAYS = [
        ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'),
    ]
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.assigned_class} - {self.subject} - {self.day}"
