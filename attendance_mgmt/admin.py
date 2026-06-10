from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance
@admin.register(StudentAttendance)
class AttAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'class_name']
    list_filter = ['status', 'date']
admin.site.register(TeacherAttendance)
