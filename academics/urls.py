from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SubjectViewSet, ExamViewSet, ResultViewSet, HomeworkViewSet, TimetableViewSet

router = DefaultRouter()
router.register('subjects', SubjectViewSet)
router.register('exams', ExamViewSet)
router.register('results', ResultViewSet)
router.register('homework', HomeworkViewSet)
router.register('timetable', TimetableViewSet)
urlpatterns = [path('', include(router.urls))]
