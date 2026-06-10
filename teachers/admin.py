from django.contrib import admin
from .models import Teacher, Department

admin.site.register(Department)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'department', 'subjects', 'status']
    list_filter = ['status', 'department']
    search_fields = ['employee_id', 'first_name', 'last_name']
