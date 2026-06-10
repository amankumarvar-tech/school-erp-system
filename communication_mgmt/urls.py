from django.urls import path
from . import views
urlpatterns = [
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.notice_add, name='notice_add'),
    path('notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/send/', views.message_send, name='message_send'),
    path('events/', views.events_list, name='events_list'),
    path('events/add/', views.event_add, name='event_add'),
]
