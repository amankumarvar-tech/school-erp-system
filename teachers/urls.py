from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TeacherViewSet, DepartmentViewSet

router = DefaultRouter()
router.register('teachers', TeacherViewSet)
router.register('departments', DepartmentViewSet)
urlpatterns = [path('', include(router.urls))]
