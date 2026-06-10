from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings_view, name='settings_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
