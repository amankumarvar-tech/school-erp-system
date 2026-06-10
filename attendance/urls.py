from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StudentAttendanceViewSet, TeacherAttendanceViewSet, LeaveApplicationViewSet

router = DefaultRouter()
router.register('student-attendance', StudentAttendanceViewSet)
router.register('teacher-attendance', TeacherAttendanceViewSet)
router.register('leave-applications', LeaveApplicationViewSet)
urlpatterns = [path('', include(router.urls))]
