from django.urls import path
from . import views
urlpatterns = [
    path('timetable/', views.timetable_list, name='timetable_list'),
]
