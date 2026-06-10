from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, Department
from django.db.models import Q

@login_required
def teacher_list(request):
    query = request.GET.get('q', '')
    teachers = Teacher.objects.filter(is_active=True).select_related('department')
    if query:
        teachers = teachers.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(employee_id__icontains=query) | Q(designation__icontains=query)
        )
    return render(request, 'teacher_mgmt/list.html', {'teachers': teachers, 'query': query})

@login_required
def teacher_add(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        try:
            Teacher.objects.create(
                employee_id=request.POST['employee_id'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                date_of_birth=request.POST['date_of_birth'],
                gender=request.POST['gender'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                designation=request.POST['designation'],
                qualification=request.POST['qualification'],
                joining_date=request.POST['joining_date'],
                experience_years=request.POST.get('experience_years', 0),
                basic_salary=request.POST.get('basic_salary', 0),
                employment_type=request.POST.get('employment_type', 'permanent'),
                department_id=request.POST.get('department') or None,
            )
            messages.success(request, 'Teacher added successfully!')
            return redirect('teacher_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'teacher_mgmt/add.html', {'departments': departments})

@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teacher_mgmt/detail.html', {'teacher': teacher})

@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher.first_name = request.POST['first_name']
        teacher.last_name = request.POST['last_name']
        teacher.email = request.POST['email']
        teacher.phone = request.POST['phone']
        teacher.designation = request.POST['designation']
        teacher.qualification = request.POST['qualification']
        teacher.experience_years = request.POST.get('experience_years', 0)
        teacher.basic_salary = request.POST.get('basic_salary', 0)
        teacher.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teacher_detail', pk=pk)
    return render(request, 'teacher_mgmt/edit.html', {'teacher': teacher, 'departments': departments})
