from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum
import datetime
from .models import SalaryStructure, SalaryPayment, Advance
from teacher_mgmt.models import Teacher

@login_required
def payroll_dashboard(request):
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    total_teachers = Teacher.objects.filter(is_active=True).count()
    paid_this_month = SalaryPayment.objects.filter(month=current_month, year=current_year, status='paid').count()
    pending_this_month = total_teachers - paid_this_month
    total_payout = SalaryPayment.objects.filter(month=current_month, year=current_year, status='paid').aggregate(t=Sum('net_salary'))['t'] or 0
    recent_payments = SalaryPayment.objects.select_related('teacher').order_by('-created_at')[:10]
    teachers_no_structure = Teacher.objects.filter(is_active=True).exclude(salary_structure__is_active=True)
    context = {
        'total_teachers': total_teachers, 'paid_this_month': paid_this_month,
        'pending_this_month': pending_this_month, 'total_payout': total_payout,
        'recent_payments': recent_payments, 'teachers_no_structure': teachers_no_structure,
        'current_month': current_month, 'current_year': current_year,
    }
    return render(request, 'payroll_mgmt/dashboard.html', context)

@login_required
def salary_structure_list(request):
    structures = SalaryStructure.objects.filter(is_active=True).select_related('teacher')
    teachers_without = Teacher.objects.filter(is_active=True).exclude(salary_structure__is_active=True)
    return render(request, 'payroll_mgmt/structure_list.html', {'structures': structures, 'teachers_without': teachers_without})

@login_required
def salary_structure_add(request):
    teachers = Teacher.objects.filter(is_active=True)
    if request.method == 'POST':
        teacher_id = request.POST['teacher']
        SalaryStructure.objects.filter(teacher_id=teacher_id, is_active=True).update(is_active=False)
        basic = float(request.POST.get('basic_salary', 0))
        SalaryStructure.objects.create(
            teacher_id=teacher_id,
            basic_salary=basic,
            hra=request.POST.get('hra', 0),
            da=request.POST.get('da', 0),
            ta=request.POST.get('ta', 0),
            medical_allowance=request.POST.get('medical_allowance', 0),
            other_allowance=request.POST.get('other_allowance', 0),
            pf_deduction=request.POST.get('pf_deduction', 0),
            esi_deduction=request.POST.get('esi_deduction', 0),
            tax_deduction=request.POST.get('tax_deduction', 0),
            other_deduction=request.POST.get('other_deduction', 0),
            effective_from=request.POST['effective_from'],
        )
        messages.success(request, 'Salary structure saved!')
        return redirect('salary_structure_list')
    return render(request, 'payroll_mgmt/structure_add.html', {'teachers': teachers})

@login_required
def generate_payroll(request):
    teachers = Teacher.objects.filter(is_active=True, salary_structure__is_active=True).distinct()
    months = [(i, datetime.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    years = [2023, 2024, 2025]
    if request.method == 'POST':
        month = int(request.POST['month'])
        year = int(request.POST['year'])
        generated = 0
        for teacher in teachers:
            structure = teacher.salary_structure.filter(is_active=True).first()
            if structure and not SalaryPayment.objects.filter(teacher=teacher, month=month, year=year).exists():
                SalaryPayment.objects.create(
                    teacher=teacher, month=month, year=year,
                    salary_structure=structure,
                    basic_salary=structure.basic_salary,
                    gross_salary=structure.gross_salary,
                    total_deductions=structure.total_deductions,
                    net_salary=structure.net_salary,
                    generated_by=request.user.get_full_name() or request.user.username,
                )
                generated += 1
        messages.success(request, f'Payroll generated for {generated} teachers for {month}/{year}!')
        return redirect('payroll_list')
    return render(request, 'payroll_mgmt/generate.html', {'teachers': teachers, 'months': months, 'years': years})

@login_required
def payroll_list(request):
    month = request.GET.get('month', datetime.date.today().month)
    year = request.GET.get('year', datetime.date.today().year)
    payments = SalaryPayment.objects.filter(month=month, year=year).select_related('teacher')
    months = [(i, datetime.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    years = [2023, 2024, 2025]
    total_net = payments.aggregate(t=Sum('net_salary'))['t'] or 0
    return render(request, 'payroll_mgmt/list.html', {
        'payments': payments, 'months': months, 'years': years,
        'month': int(month), 'year': int(year), 'total_net': total_net,
    })

@login_required
def mark_salary_paid(request, pk):
    payment = get_object_or_404(SalaryPayment, pk=pk)
    if request.method == 'POST':
        payment.status = 'paid'
        payment.payment_date = datetime.date.today()
        payment.payment_method = request.POST.get('payment_method', 'bank')
        payment.transaction_id = request.POST.get('transaction_id', '')
        payment.save()
        messages.success(request, f'Salary marked as paid for {payment.teacher.full_name}!')
        return redirect('payroll_list')
    return render(request, 'payroll_mgmt/mark_paid.html', {'payment': payment})
