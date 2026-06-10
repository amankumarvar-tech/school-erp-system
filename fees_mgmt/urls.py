from django.urls import path
from . import views
urlpatterns = [
    path('', views.fees_list, name='fees_list'),
    path('add/', views.fees_add, name='fees_add'),
    path('<int:pk>/', views.fees_detail, name='fees_detail'),
]
