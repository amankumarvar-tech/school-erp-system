from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import io

def get_reportlab():
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        return canvas, A4, colors, cm
    except ImportError:
        return None, None, None, None

@login_required
def fee_receipt_pdf(request, payment_id):
    canvas_mod, A4, colors, cm = get_reportlab()
    if not canvas_mod:
        from django.http import HttpResponse
        return HttpResponse("reportlab not installed. Run: pip install reportlab", status=500)

    from fees_mgmt.models import FeePayment
    from core.models import SchoolProfile
    payment = get_object_or_404(FeePayment, pk=payment_id)
    school = SchoolProfile.objects.first()

    buffer = io.BytesIO()
    c = canvas_mod.Canvas(buffer, pagesize=A4)
    w, h = A4

    # Header bar
    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.rect(0, h - 100, w, 100, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 20)
    school_name = school.name if school else "School ERP"
    c.drawCentredString(w / 2, h - 45, school_name)
    c.setFont("Helvetica", 10)
    if school:
        c.drawCentredString(w / 2, h - 65, f"{school.address} | {school.phone}")
    c.drawCentredString(w / 2, h - 82, "FEE PAYMENT RECEIPT")

    # Receipt box
    c.setFillColorRGB(0.95, 0.97, 1)
    c.roundRect(1.5 * cm, h - 180, w - 3 * cm, 65, 8, fill=1, stroke=0)
    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, h - 130, f"Receipt No: FEE-{payment.id:05d}")
    c.setFont("Helvetica", 11)
    c.drawString(2 * cm, h - 148, f"Date: {payment.payment_date or 'N/A'}")
    c.drawString(10 * cm, h - 130, f"Status: {payment.get_status_display()}")
    c.drawString(10 * cm, h - 148, f"Method: {payment.get_payment_method_display() if hasattr(payment, 'get_payment_method_display') else '-'}")

    # Student details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, h - 210, "Student Details")
    c.setStrokeColorRGB(0.23, 0.31, 0.85)
    c.line(2 * cm, h - 213, 8 * cm, h - 213)

    c.setFont("Helvetica", 11)
    rows = [
        ("Student Name:", payment.student.full_name),
        ("Admission No:", payment.student.admission_number),
        ("Class:", str(payment.student.current_class) if payment.student.current_class else "N/A"),
        ("Father Name:", payment.student.father_name),
    ]
    y = h - 230
    for label, val in rows:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2 * cm, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(7 * cm, y, val)
        y -= 18

    # Fee details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y - 10, "Fee Details")
    c.setStrokeColorRGB(0.23, 0.31, 0.85)
    c.line(2 * cm, y - 13, 7 * cm, y - 13)
    y -= 30

    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.rect(2 * cm, y, w - 4 * cm, 22, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.3 * cm, y + 6, "Description")
    c.drawString(12 * cm, y + 6, "Amount")
    y -= 20

    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.setFont("Helvetica", 10)
    fee_type = payment.fee_structure.fee_type if hasattr(payment, 'fee_structure') and payment.fee_structure else "School Fee"
    c.drawString(2.3 * cm, y, str(fee_type))
    c.drawString(12 * cm, y, f"Rs. {payment.total_amount}")
    y -= 18
    if payment.discount_amount:
        c.setFillColorRGB(0.04, 0.6, 0.44)
        c.drawString(2.3 * cm, y, "Discount")
        c.drawString(12 * cm, y, f"- Rs. {payment.discount_amount}")
        c.setFillColorRGB(0.1, 0.12, 0.21)
        y -= 18

    c.setStrokeColorRGB(0.85, 0.88, 0.95)
    c.line(2 * cm, y, w - 2 * cm, y)
    y -= 16

    c.setFillColorRGB(0.23, 0.31, 0.85)
    c.rect(2 * cm, y - 8, w - 4 * cm, 26, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2.3 * cm, y + 4, "Amount Paid")
    c.drawString(12 * cm, y + 4, f"Rs. {payment.amount_paid}")
    y -= 45

    if payment.fine_amount:
        c.setFillColorRGB(0.9, 0.3, 0.2)
        c.setFont("Helvetica", 10)
        c.drawString(2.3 * cm, y, f"Fine: Rs. {payment.fine_amount}")
        y -= 18

    # Footer
    c.setFillColorRGB(0.55, 0.55, 0.6)
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, 2.5 * cm, "This is a computer generated receipt. No signature required.")
    c.drawCentredString(w / 2, 1.8 * cm, f"Generated on: {timezone.now().strftime('%d-%m-%Y %H:%M')}")

    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="fee_receipt_{payment.id}.pdf"'
    return response


@login_required
def transfer_certificate_pdf(request, student_id):
    canvas_mod, A4, colors, cm = get_reportlab()
    if not canvas_mod:
        return HttpResponse("reportlab not installed. Run: pip install reportlab", status=500)

    from student_mgmt.models import Student
    from core.models import SchoolProfile
    student = get_object_or_404(Student, pk=student_id)
    school = SchoolProfile.objects.first()

    buffer = io.BytesIO()
    c = canvas_mod.Canvas(buffer, pagesize=A4)
    w, h = A4

    # Border
    c.setStrokeColorRGB(0.23, 0.31, 0.85)
    c.setLineWidth(3)
    c.rect(1 * cm, 1 * cm, w - 2 * cm, h - 2 * cm)
    c.setLineWidth(1)
    c.setStrokeColorRGB(0.7, 0.75, 0.9)
    c.rect(1.3 * cm, 1.3 * cm, w - 2.6 * cm, h - 2.6 * cm)

    # Header
    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w / 2, h - 4 * cm, school.name if school else "School ERP")
    c.setFont("Helvetica", 10)
    if school:
        c.drawCentredString(w / 2, h - 4.8 * cm, f"{school.address} | Ph: {school.phone} | {school.board} Board")

    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.23, 0.31, 0.85)
    c.drawCentredString(w / 2, h - 6 * cm, "TRANSFER CERTIFICATE")
    c.setStrokeColorRGB(0.23, 0.31, 0.85)
    c.setLineWidth(2)
    c.line(6 * cm, h - 6.3 * cm, w - 6 * cm, h - 6.3 * cm)
    c.setLineWidth(1)

    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, h - 7.2 * cm, f"TC No: TC-{student.id:04d}-{timezone.now().year}")
    c.drawString(13 * cm, h - 7.2 * cm, f"Date: {timezone.now().strftime('%d-%m-%Y')}")

    # Student info
    fields = [
        ("1.", "Name of Student", student.full_name),
        ("2.", "Father's Name", student.father_name),
        ("3.", "Mother's Name", student.mother_name),
        ("4.", "Date of Birth", str(student.date_of_birth)),
        ("5.", "Admission Number", student.admission_number),
        ("6.", "Class Last Studied", str(student.current_class) if student.current_class else "N/A"),
        ("7.", "Category", student.get_category_display()),
        ("8.", "Date of Admission", str(student.admission_date)),
        ("9.", "Reason for Leaving", "As per parent's request"),
        ("10.", "Last Attendance Date", timezone.now().strftime('%d-%m-%Y')),
    ]
    y = h - 8.5 * cm
    for num, label, val in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2 * cm, y, num)
        c.drawString(2.8 * cm, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(9 * cm, y, ": " + val)
        c.setStrokeColorRGB(0.85, 0.88, 0.95)
        c.line(2 * cm, y - 4, w - 2 * cm, y - 4)
        y -= 0.75 * cm

    # Conduct certificate
    y -= 0.5 * cm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, y, "Character & Conduct:")
    c.setFont("Helvetica", 10)
    c.drawString(7 * cm, y, "Good")

    # Signature section
    y = 5 * cm
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, "Class Teacher")
    c.drawString(w / 2 - 2 * cm, y, "Exam Controller")
    c.drawString(w - 6 * cm, y, "Principal")

    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    for x in [2 * cm, w / 2 - 2 * cm, w - 6 * cm]:
        c.line(x, y + 1.5 * cm, x + 3.5 * cm, y + 1.5 * cm)

    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.55, 0.55, 0.6)
    c.drawCentredString(w / 2, 2 * cm, "This is a computer generated Transfer Certificate.")

    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="TC_{student.admission_number}.pdf"'
    return response


@login_required
def id_card_pdf(request, student_id):
    canvas_mod, A4, colors, cm = get_reportlab()
    if not canvas_mod:
        return HttpResponse("reportlab not installed. Run: pip install reportlab", status=500)

    from student_mgmt.models import Student
    from core.models import SchoolProfile
    student = get_object_or_404(Student, pk=student_id)
    school = SchoolProfile.objects.first()

    buffer = io.BytesIO()
    c = canvas_mod.Canvas(buffer, pagesize=A4)
    w, h = A4

    # Card dimensions (CR80 card: 85.6mm x 54mm scaled up)
    card_w = 9 * cm
    card_h = 5.8 * cm
    cx = (w - card_w) / 2
    cy = (h - card_h) / 2

    # Card background
    c.setFillColorRGB(0.97, 0.97, 1)
    c.roundRect(cx, cy, card_w, card_h, 8, fill=1, stroke=0)
    c.setStrokeColorRGB(0.23, 0.31, 0.85)
    c.setLineWidth(1.5)
    c.roundRect(cx, cy, card_w, card_h, 8, fill=0, stroke=1)

    # Header band
    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.rect(cx, cy + card_h - 1.4 * cm, card_w, 1.4 * cm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(cx + card_w / 2, cy + card_h - 0.7 * cm, school.name if school else "SCHOOL ERP")
    c.setFont("Helvetica", 6)
    c.drawCentredString(cx + card_w / 2, cy + card_h - 1.15 * cm, "STUDENT IDENTITY CARD")

    # Photo placeholder
    c.setFillColorRGB(0.85, 0.87, 0.95)
    c.rect(cx + 0.3 * cm, cy + 0.5 * cm, 1.8 * cm, 2.3 * cm, fill=1, stroke=0)
    c.setFillColorRGB(0.5, 0.5, 0.6)
    c.setFont("Helvetica", 7)
    c.drawCentredString(cx + 1.2 * cm, cy + 1.6 * cm, "Photo")

    # Student Info
    c.setFillColorRGB(0.1, 0.12, 0.21)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(cx + 2.4 * cm, cy + card_h - 1.9 * cm, student.full_name)
    info = [
        ("Adm No:", student.admission_number),
        ("Class:", str(student.current_class) if student.current_class else "N/A"),
        ("DOB:", str(student.date_of_birth)),
        ("Father:", student.father_name[:20]),
        ("Phone:", student.father_phone),
    ]
    y = cy + card_h - 2.4 * cm
    for label, val in info:
        c.setFont("Helvetica-Bold", 7)
        c.drawString(cx + 2.4 * cm, y, label)
        c.setFont("Helvetica", 7)
        c.drawString(cx + 4.2 * cm, y, val)
        y -= 0.42 * cm

    # Footer
    c.setFillColorRGB(0.23, 0.31, 0.85)
    c.rect(cx, cy, card_w, 0.6 * cm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica", 6)
    c.drawCentredString(cx + card_w / 2, cy + 0.18 * cm, f"If found, return to school | {school.phone if school else ''}")

    c.setFillColorRGB(0.55, 0.55, 0.6)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, 2.5 * cm, f"Student ID Card — {student.full_name}")

    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ID_{student.admission_number}.pdf"'
    return response
