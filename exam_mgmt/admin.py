from django.contrib import admin
from .models import ExamType, Exam, ExamResult, ReportCard
admin.site.register(ExamType)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(ReportCard)
