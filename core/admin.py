from django.contrib import admin
from .models import SchoolProfile, AcademicYear, UserProfile
admin.site.register(SchoolProfile)
admin.site.register(AcademicYear)
admin.site.register(UserProfile)
admin.site.site_header = "EduManage School ERP"
admin.site.site_title = "School ERP Admin"
admin.site.index_title = "Welcome to School ERP Administration"
