from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StudentViewSet, ClassViewSet

router = DefaultRouter()
router.register('students', StudentViewSet)
router.register('classes', ClassViewSet)
urlpatterns = [path('', include(router.urls))]
