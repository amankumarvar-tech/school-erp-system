from django.db import models
from core.models import AcademicYear

class Subject(models.Model):
    SUBJECT_TYPES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('language', 'Language'),
        ('co_curricular', 'Co-Curricular'),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES, default='theory')
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=33)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class ClassSubject(models.Model):
    class_name = models.ForeignKey('student_mgmt.Class', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_mandatory = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['class_name', 'subject']

class Timetable(models.Model):
    DAYS = [
        ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'),
        ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'),
    ]
    
    class_name = models.ForeignKey('student_mgmt.Class', on_delete=models.CASCADE, related_name='timetable')
    day = models.CharField(max_length=3, choices=DAYS)
    period_number = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('teacher_mgmt.Teacher', on_delete=models.SET_NULL, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20, blank=True)
    
    class Meta:
        unique_together = ['class_name', 'day', 'period_number']
    
    def __str__(self):
        return f"{self.class_name} - {self.day} Period {self.period_number}"

class Holiday(models.Model):
    HOLIDAY_TYPES = [
        ('national', 'National Holiday'),
        ('regional', 'Regional Holiday'),
        ('school', 'School Holiday'),
        ('exam', 'Exam'),
        ('event', 'School Event'),
    ]
    name = models.CharField(max_length=100)
    date = models.DateField()
    holiday_type = models.CharField(max_length=20, choices=HOLIDAY_TYPES)
    description = models.TextField(blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.date}"

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.ForeignKey('student_mgmt.Class', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey('teacher_mgmt.Teacher', on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    max_marks = models.IntegerField(default=10)
    attachment = models.FileField(upload_to='assignments/', blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.class_name}"
