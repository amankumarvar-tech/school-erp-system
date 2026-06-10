from django.urls import path
from . import views

urlpatterns = [
    path('', views.import_home, name='import_home'),
    path('students/', views.import_students, name='import_students'),
    path('teachers/', views.import_teachers, name='import_teachers'),
    path('fees/', views.import_fees, name='import_fees'),
    path('template/', views.download_template, name='download_template'),
]
