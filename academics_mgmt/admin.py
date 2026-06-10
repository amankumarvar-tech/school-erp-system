from django.contrib import admin
from .models import Subject, ClassSubject, Timetable, Holiday, Assignment
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(Holiday)
admin.site.register(Assignment)
