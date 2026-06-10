from django.urls import path
from . import views
urlpatterns = [
    path('', views.payroll_dashboard, name='payroll_dashboard'),
    path('structures/', views.salary_structure_list, name='salary_structure_list'),
    path('structures/add/', views.salary_structure_add, name='salary_structure_add'),
    path('generate/', views.generate_payroll, name='generate_payroll'),
    path('list/', views.payroll_list, name='payroll_list'),
    path('pay/<int:pk>/', views.mark_salary_paid, name='mark_salary_paid'),
]
