from django.urls import path
from . import views
from .pdf_views import fee_receipt_pdf, transfer_certificate_pdf, id_card_pdf

urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('students/pdf/', views.student_report_pdf, name='student_report_pdf'),
    path('attendance/pdf/', views.attendance_report_pdf, name='attendance_report_pdf'),
    path('fees/pdf/', views.fee_report_pdf, name='fee_report_pdf'),
    path('results/<int:exam_id>/pdf/', views.result_report_pdf, name='result_report_pdf'),
    path('salary/<int:payment_id>/slip/', views.salary_slip_pdf, name='salary_slip_pdf'),
    # New PDF endpoints
    path('fee-receipt/<int:payment_id>/', fee_receipt_pdf, name='fee_receipt_pdf'),
    path('tc/<int:student_id>/', transfer_certificate_pdf, name='transfer_certificate_pdf'),
    path('id-card/<int:student_id>/', id_card_pdf, name='id_card_pdf'),
]
