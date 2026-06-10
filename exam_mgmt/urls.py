from django.urls import path
from . import views
urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.exam_add, name='exam_add'),
    path('<int:exam_id>/results/', views.result_entry, name='result_entry'),
]
