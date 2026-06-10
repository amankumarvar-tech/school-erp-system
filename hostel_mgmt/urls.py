from django.urls import path
from . import views
urlpatterns = [
    path('', views.hostel_dashboard, name='hostel_dashboard'),
    path('add/', views.hostel_add, name='hostel_add'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('allocate/', views.allocate_room, name='allocate_room'),
]
