from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FeePayment, FeeStructure
from student_mgmt.models import Student

@login_required
def fees_list(request):
    status = request.GET.get('status', '')
    fees = FeePayment.objects.select_related('student', 'fee_structure').order_by('-created_at')
    if status:
        fees = fees.filter(status=status)
    return render(request, 'fees_mgmt/list.html', {'fees': fees, 'status': status})

@login_required
def fees_add(request):
    students = Student.objects.filter(is_active=True)
    structures = FeeStructure.objects.all()
    if request.method == 'POST':
        import random, string
        receipt = 'RCP' + ''.join(random.choices(string.digits, k=8))
        try:
            FeePayment.objects.create(
                student_id=request.POST['student'],
                fee_structure_id=request.POST['fee_structure'],
                amount_due=request.POST['amount_due'],
                amount_paid=request.POST['amount_paid'],
                due_date=request.POST['due_date'],
                payment_date=request.POST.get('payment_date') or None,
                payment_method=request.POST.get('payment_method', ''),
                transaction_id=request.POST.get('transaction_id', ''),
                status=request.POST.get('status', 'paid'),
                receipt_number=receipt,
                collected_by=request.user.get_full_name() or request.user.username,
            )
            messages.success(request, f'Fee payment recorded! Receipt: {receipt}')
            return redirect('fees_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'fees_mgmt/add.html', {'students': students, 'structures': structures})

@login_required
def fees_detail(request, pk):
    fee = get_object_or_404(FeePayment, pk=pk)
    return render(request, 'fees_mgmt/detail.html', {'fee': fee})
