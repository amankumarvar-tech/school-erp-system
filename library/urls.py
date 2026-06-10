from django.urls import path
from . import views
urlpatterns = [
    path('', views.library_dashboard, name='library_dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('issue/', views.issue_book, name='issue_book'),
    path('return/<int:issue_id>/', views.return_book, name='return_book'),
    path('issues/', views.issue_list, name='issue_list'),
]
