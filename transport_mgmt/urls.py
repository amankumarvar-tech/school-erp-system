from django.urls import path
from . import views
urlpatterns = [
    path('', views.transport_dashboard, name='transport_dashboard'),
    path('route/add/', views.route_add, name='route_add'),
    path('assign/', views.assign_transport, name='assign_transport'),
]
