from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.dashboard, name='dashboard'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('students/', include('student_mgmt.urls')),
    path('teachers/', include('teacher_mgmt.urls')),
    path('academics/', include('academics_mgmt.urls')),
    path('attendance/', include('attendance_mgmt.urls')),
    path('fees/', include('fees_mgmt.urls')),
    path('exams/', include('exam_mgmt.urls')),
    path('communication/', include('communication_mgmt.urls')),
    path('library/', include('library.urls')),
    path('payroll/', include('payroll_mgmt.urls')),
    path('reports/', include('reports_mgmt.urls')),
    path('analytics/', include('analytics_mgmt.urls')),
    path('core/', include('core.urls')),
    path('transport/', include('transport_mgmt.urls')),
    path('hostel/', include('hostel_mgmt.urls')),
    path('import/', include('excel_import.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
