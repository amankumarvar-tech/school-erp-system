from django.db import models
from student_mgmt.models import Student
from teacher_mgmt.models import Teacher

class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Book(models.Model):
    CONDITION_CHOICES = [('new','New'),('good','Good'),('fair','Fair'),('poor','Poor')]
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    shelf_location = models.CharField(max_length=50, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    cover_image = models.ImageField(upload_to='books/', blank=True)
    description = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"{self.title} by {self.author}"

class BookIssue(models.Model):
    STATUS_CHOICES = [('issued','Issued'),('returned','Returned'),('overdue','Overdue'),('lost','Lost')]
    BORROWER_TYPE = [('student','Student'),('teacher','Teacher')]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    borrower_type = models.CharField(max_length=10, choices=BORROWER_TYPE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='borrowed_books')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='borrowed_books')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fine_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    issued_by = models.CharField(max_length=100, blank=True)
    def __str__(self):
        borrower = self.student or self.teacher
        return f"{self.book.title} → {borrower}"
    @property
    def borrower_name(self):
        if self.student: return self.student.full_name
        if self.teacher: return self.teacher.full_name
        return "Unknown"
