from django.contrib import admin
from .models import Teacher, Department, TeacherLeave, TeacherSubject
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'designation', 'department', 'is_active']
    search_fields = ['first_name', 'last_name', 'employee_id']
admin.site.register(Department)
admin.site.register(TeacherLeave)
admin.site.register(TeacherSubject)
