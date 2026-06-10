from django.contrib import admin
from .models import Student, Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['grade', 'section', 'class_teacher', 'capacity']
    ordering = ['grade', 'section']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_no', 'full_name', 'current_class', 'gender', 'status']
    list_filter = ['status', 'gender', 'current_class']
    search_fields = ['admission_no', 'first_name', 'last_name']
    ordering = ['admission_no']
