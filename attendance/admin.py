from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance, LeaveApplication
admin.site.register(StudentAttendance)
admin.site.register(TeacherAttendance)
admin.site.register(LeaveApplication)
