from django.contrib import admin
from .models import Student, Class, StudentDocument
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'full_name', 'current_class', 'father_name', 'is_active']
    list_filter = ['gender', 'current_class', 'is_active', 'category']
    search_fields = ['first_name', 'last_name', 'admission_number', 'father_name']
admin.site.register(Class)
admin.site.register(StudentDocument)
