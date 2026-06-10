from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import datetime, io
from student_mgmt.models import Student, Class
from teacher_mgmt.models import Teacher
from attendance_mgmt.models import StudentAttendance
from fees_mgmt.models import FeePayment
from exam_mgmt.models import ExamResult, Exam

def make_pdf_response(filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

def header_style(): return ParagraphStyle('header', fontSize=18, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=colors.HexColor('#1a1f36'))
def sub_style(): return ParagraphStyle('sub', fontSize=11, fontName='Helvetica', alignment=TA_CENTER, textColor=colors.HexColor('#8892a4'))
def title_style(): return ParagraphStyle('title', fontSize=13, fontName='Helvetica-Bold', textColor=colors.HexColor('#1a1f36'), spaceAfter=4)
def normal_style(): return ParagraphStyle('normal', fontSize=10, fontName='Helvetica', textColor=colors.HexColor('#374151'))

TABLE_HEADER_STYLE = [
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1f36')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7f8fc')]),
    ('FONTSIZE', (0,1), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e2e8f0')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]

@login_required
def reports_home(request):
    return render(request, 'reports_mgmt/home.html')

@login_required
def student_report_pdf(request):
    class_id = request.GET.get('class_id')
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("🏫 EduManage School ERP", header_style()))
    elements.append(Paragraph("Student Master Report", sub_style()))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3b4fd8')))
    elements.append(Spacer(1, 10))
    students = Student.objects.filter(is_active=True).select_related('current_class')
    if class_id:
        students = students.filter(current_class_id=class_id)
    data = [['Adm. No.', 'Student Name', 'Gender', 'Class', 'DOB', 'Father Name', 'Father Phone', 'Blood Group', 'Category']]
    for s in students:
        data.append([
            s.admission_number, s.full_name, s.get_gender_display(),
            str(s.current_class or '—'), str(s.date_of_birth),
            s.father_name, s.father_phone, s.blood_group or '—', s.get_category_display()
        ])
    col_widths = [2*cm, 4*cm, 1.8*cm, 2.5*cm, 2.2*cm, 3.5*cm, 2.8*cm, 2*cm, 1.8*cm]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(TABLE_HEADER_STYLE))
    elements.append(t)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%d %b %Y %H:%M')} | Total: {len(data)-1} students", normal_style()))
    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="student_report.pdf"'
    return response

@login_required
def attendance_report_pdf(request):
    class_id = request.GET.get('class_id')
    date_from = request.GET.get('from', str(datetime.date.today().replace(day=1)))
    date_to = request.GET.get('to', str(datetime.date.today()))
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    elements = []
    elements.append(Paragraph("🏫 EduManage School ERP", header_style()))
    elements.append(Paragraph(f"Attendance Report: {date_from} to {date_to}", sub_style()))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3b4fd8')))
    elements.append(Spacer(1, 10))
    students = Student.objects.filter(is_active=True).select_related('current_class')
    if class_id:
        students = students.filter(current_class_id=class_id)
    data = [['Student Name', 'Class', 'Total Days', 'Present', 'Absent', 'Late', 'Attendance %']]
    for student in students:
        att = StudentAttendance.objects.filter(student=student, date__range=[date_from, date_to])
        total = att.count()
        present = att.filter(status='present').count()
        absent = att.filter(status='absent').count()
        late = att.filter(status='late').count()
        pct = f"{(present/total*100):.1f}%" if total > 0 else "N/A"
        data.append([student.full_name, str(student.current_class or '—'), total, present, absent, late, pct])
    t = Table(data, colWidths=[5*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 3*cm], repeatRows=1)
    t.setStyle(TableStyle(TABLE_HEADER_STYLE + [('ALIGN', (2,1), (-1,-1), 'CENTER')]))
    elements.append(t)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}", normal_style()))
    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="attendance_report.pdf"'
    return response

@login_required
def fee_report_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    elements = []
    elements.append(Paragraph("🏫 EduManage School ERP", header_style()))
    elements.append(Paragraph("Fee Collection Report", sub_style()))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3b4fd8')))
    elements.append(Spacer(1, 10))
    payments = FeePayment.objects.select_related('student', 'fee_structure').order_by('due_date')
    total_due = payments.aggregate(t=Sum('amount_due'))['t'] or 0
    total_paid = payments.aggregate(t=Sum('amount_paid'))['t'] or 0
    summary = [['Total Due', 'Total Collected', 'Balance', 'Paid Count', 'Pending Count']]
    summary.append([f"₹{total_due:,.0f}", f"₹{total_paid:,.0f}", f"₹{total_due-total_paid:,.0f}",
                    payments.filter(status='paid').count(), payments.filter(status__in=['pending','overdue']).count()])
    st = Table(summary, colWidths=[3.5*cm]*5)
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3b4fd8')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#f0f2ff')),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
    ]))
    elements.append(st)
    elements.append(Spacer(1, 12))
    data = [['Receipt No.', 'Student', 'Fee Type', 'Amount Due', 'Paid', 'Balance', 'Due Date', 'Status']]
    for p in payments:
        status_map = {'paid': 'PAID', 'pending': 'PENDING', 'overdue': 'OVERDUE', 'partial': 'PARTIAL'}
        data.append([
            p.receipt_number or '—', p.student.full_name,
            p.fee_structure.get_fee_type_display(),
            f"₹{p.amount_due:,.0f}", f"₹{p.amount_paid:,.0f}",
            f"₹{p.balance:,.0f}", str(p.due_date),
            status_map.get(p.status, p.status)
        ])
    t = Table(data, colWidths=[2.5*cm, 4*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.2*cm], repeatRows=1)
    style = TableStyle(TABLE_HEADER_STYLE)
    for i, row in enumerate(data[1:], 1):
        if row[-1] == 'OVERDUE':
            style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor('#e74c3c'))
            style.add('FONTNAME', (7, i), (7, i), 'Helvetica-Bold')
        elif row[-1] == 'PAID':
            style.add('TEXTCOLOR', (7, i), (7, i), colors.HexColor('#2ecc71'))
            style.add('FONTNAME', (7, i), (7, i), 'Helvetica-Bold')
    t.setStyle(style)
    elements.append(t)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}", normal_style()))
    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="fee_report.pdf"'
    return response

@login_required
def result_report_pdf(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    results = ExamResult.objects.filter(exam=exam).select_related('student').order_by('-marks_obtained')
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    elements.append(Paragraph("🏫 EduManage School ERP", header_style()))
    elements.append(Paragraph(f"Exam Result: {exam.subject.name} | {exam.exam_type.name}", sub_style()))
    elements.append(Paragraph(f"Class: {exam.class_name} | Date: {exam.exam_date} | Max Marks: {exam.max_marks}", sub_style()))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3b4fd8')))
    elements.append(Spacer(1, 10))
    if results:
        passed = results.filter(marks_obtained__gte=exam.pass_marks).count()
        failed = results.filter(marks_obtained__lt=exam.pass_marks).count()
        avg = results.aggregate(a=Avg('marks_obtained'))['a'] or 0
        highest = results.first().marks_obtained if results else 0
        summary = [['Total Students', 'Passed', 'Failed', 'Average Marks', 'Highest Marks', 'Pass %']]
        summary.append([results.count(), passed, failed, f"{avg:.1f}", str(highest), f"{passed/results.count()*100:.1f}%"])
        st = Table(summary, colWidths=[3*cm]*6)
        st.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1f36')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#f0f2ff')),
        ]))
        elements.append(st)
        elements.append(Spacer(1, 12))
    data = [['Rank', 'Student Name', 'Marks Obtained', f'Out of {exam.max_marks}', 'Percentage', 'Grade', 'Status']]
    for i, r in enumerate(results, 1):
        pct = (float(r.marks_obtained) / exam.max_marks * 100)
        passed = r.marks_obtained >= exam.pass_marks
        data.append([str(i), r.student.full_name, str(r.marks_obtained), str(exam.max_marks),
                     f"{pct:.1f}%", r.grade, 'PASS' if passed else 'FAIL'])
    t = Table(data, colWidths=[1.5*cm, 5.5*cm, 3*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm], repeatRows=1)
    style = TableStyle(TABLE_HEADER_STYLE)
    for i, row in enumerate(data[1:], 1):
        if row[-1] == 'FAIL':
            style.add('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#e74c3c'))
            style.add('FONTNAME', (6, i), (6, i), 'Helvetica-Bold')
        else:
            style.add('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#2ecc71'))
            style.add('FONTNAME', (6, i), (6, i), 'Helvetica-Bold')
    t.setStyle(style)
    elements.append(t)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}", normal_style()))
    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="result_{exam_id}.pdf"'
    return response

@login_required
def salary_slip_pdf(request, payment_id):
    from payroll_mgmt.models import SalaryPayment
    payment = get_object_or_404(SalaryPayment, pk=payment_id)
    import calendar
    month_name = calendar.month_name[payment.month]
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    elements.append(Paragraph("🏫 EduManage School ERP", header_style()))
    elements.append(Paragraph(f"SALARY SLIP — {month_name} {payment.year}", sub_style()))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3b4fd8')))
    elements.append(Spacer(1, 12))
    emp_data = [
        ['Employee Name:', payment.teacher.full_name, 'Employee ID:', payment.teacher.employee_id],
        ['Designation:', payment.teacher.designation, 'Department:', str(payment.teacher.department or '—')],
        ['Working Days:', str(payment.working_days), 'Present Days:', str(payment.present_days)],
        ['Payment Mode:', payment.get_payment_method_display(), 'Payment Date:', str(payment.payment_date or '—')],
    ]
    emp_t = Table(emp_data, colWidths=[4*cm, 6*cm, 4*cm, 5*cm])
    emp_t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#1a1f36')),
        ('TEXTCOLOR', (2,0), (2,-1), colors.HexColor('#1a1f36')),
    ]))
    elements.append(emp_t)
    elements.append(Spacer(1, 12))
    structure = payment.salary_structure
    earn_data = [['EARNINGS', 'Amount (₹)', 'DEDUCTIONS', 'Amount (₹)']]
    if structure:
        earn_data += [
            ['Basic Salary', f"₹{structure.basic_salary:,.0f}", 'PF Deduction', f"₹{structure.pf_deduction:,.0f}"],
            ['HRA', f"₹{structure.hra:,.0f}", 'ESI Deduction', f"₹{structure.esi_deduction:,.0f}"],
            ['DA', f"₹{structure.da:,.0f}", 'Tax (TDS)', f"₹{structure.tax_deduction:,.0f}"],
            ['TA', f"₹{structure.ta:,.0f}", 'Other Deductions', f"₹{structure.other_deduction:,.0f}"],
            ['Medical Allow.', f"₹{structure.medical_allowance:,.0f}", '', ''],
            ['Other Allow.', f"₹{structure.other_allowance:,.0f}", '', ''],
        ]
    earn_data.append(['GROSS SALARY', f"₹{payment.gross_salary:,.0f}", 'TOTAL DEDUCTIONS', f"₹{payment.total_deductions:,.0f}"])
    et = Table(earn_data, colWidths=[5*cm, 4*cm, 5*cm, 4*cm])
    et.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#2ecc71')),
        ('BACKGROUND', (2,0), (3,0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,-1), (1,-1), colors.HexColor('#d1fae5')),
        ('BACKGROUND', (2,-1), (3,-1), colors.HexColor('#fee2e2')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(et)
    elements.append(Spacer(1, 12))
    net_t = Table([['NET SALARY PAYABLE', f"₹ {payment.net_salary:,.2f}"]], colWidths=[9*cm, 9*cm])
    net_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1f36')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 13),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    elements.append(net_t)
    elements.append(Spacer(1, 30))
    sig_data = [['____________________', '', '____________________'],
                ['Employee Signature', '', 'Principal/HR Signature']]
    sig_t = Table(sig_data, colWidths=[7*cm, 4*cm, 7*cm])
    sig_t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor('#8892a4')),
    ]))
    elements.append(sig_t)
    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="salary_slip_{payment.teacher.employee_id}_{payment.month}_{payment.year}.pdf"'
    return response
