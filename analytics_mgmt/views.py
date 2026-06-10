from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
import datetime, json

@login_required
def analytics_dashboard(request):
    return render(request, 'analytics_mgmt/dashboard.html')

@login_required
def chart_data(request):
    from student_mgmt.models import Student, Class
    from attendance_mgmt.models import StudentAttendance
    from fees_mgmt.models import FeePayment
    from exam_mgmt.models import ExamResult
    from teacher_mgmt.models import Teacher

    chart_type = request.GET.get('type', 'overview')
    today = datetime.date.today()

    if chart_type == 'overview':
        # Students by class
        class_data = Class.objects.annotate(count=Count('student')).values('name','section','count')
        labels = [f"Class {c['name']}-{c['section']}" for c in class_data]
        values = [c['count'] for c in class_data]
        return JsonResponse({'labels': labels, 'values': values, 'title': 'Students per Class'})

    elif chart_type == 'attendance_trend':
        # Last 7 days attendance
        labels, present_vals, absent_vals = [], [], []
        for i in range(6, -1, -1):
            day = today - datetime.timedelta(days=i)
            att = StudentAttendance.objects.filter(date=day)
            present = att.filter(status='present').count()
            absent = att.filter(status='absent').count()
            labels.append(day.strftime('%d %b'))
            present_vals.append(present)
            absent_vals.append(absent)
        return JsonResponse({'labels': labels, 'present': present_vals, 'absent': absent_vals, 'title': 'Attendance Trend (7 days)'})

    elif chart_type == 'fee_status':
        paid = FeePayment.objects.filter(status='paid').count()
        pending = FeePayment.objects.filter(status='pending').count()
        overdue = FeePayment.objects.filter(status='overdue').count()
        partial = FeePayment.objects.filter(status='partial').count()
        return JsonResponse({'labels': ['Paid','Pending','Overdue','Partial'], 'values': [paid, pending, overdue, partial]})

    elif chart_type == 'fee_monthly':
        months, amounts = [], []
        for m in range(1, today.month+1):
            total = FeePayment.objects.filter(payment_date__month=m, payment_date__year=today.year, status='paid').aggregate(t=Sum('amount_paid'))['t'] or 0
            months.append(datetime.date(2000, m, 1).strftime('%b'))
            amounts.append(float(total))
        return JsonResponse({'labels': months, 'values': amounts, 'title': 'Monthly Fee Collection'})

    elif chart_type == 'gender':
        from student_mgmt.models import Student
        male = Student.objects.filter(gender='M', is_active=True).count()
        female = Student.objects.filter(gender='F', is_active=True).count()
        other = Student.objects.filter(gender='O', is_active=True).count()
        return JsonResponse({'labels': ['Male','Female','Other'], 'values': [male, female, other]})

    elif chart_type == 'category':
        from student_mgmt.models import Student
        cats = Student.objects.filter(is_active=True).values('category').annotate(count=Count('id'))
        labels = [c['category'] for c in cats]
        values = [c['count'] for c in cats]
        return JsonResponse({'labels': labels, 'values': values, 'title': 'Students by Category'})

    elif chart_type == 'exam_performance':
        from exam_mgmt.models import ExamResult
        grade_order = ['A+','A','B+','B','C','D','E','F']
        data = ExamResult.objects.values('grade').annotate(count=Count('id'))
        grade_map = {d['grade']: d['count'] for d in data}
        labels = [g for g in grade_order if g in grade_map]
        values = [grade_map[g] for g in labels]
        return JsonResponse({'labels': labels, 'values': values, 'title': 'Exam Grade Distribution'})

    return JsonResponse({'error': 'Unknown chart type'})
