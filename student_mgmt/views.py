from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Class, StudentDocument
from django.db.models import Q

@login_required
def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.filter(is_active=True).select_related('current_class')
    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(admission_number__icontains=query) | Q(father_name__icontains=query)
        )
    return render(request, 'student_mgmt/list.html', {'students': students, 'query': query})

@login_required
def student_add(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            student = Student(
                admission_number=request.POST['admission_number'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                date_of_birth=request.POST['date_of_birth'],
                gender=request.POST['gender'],
                address=request.POST['address'],
                father_name=request.POST['father_name'],
                father_phone=request.POST['father_phone'],
                mother_name=request.POST['mother_name'],
                admission_date=request.POST['admission_date'],
                blood_group=request.POST.get('blood_group', ''),
                category=request.POST.get('category', 'GEN'),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                mother_phone=request.POST.get('mother_phone', ''),
            )
            class_id = request.POST.get('current_class')
            if class_id:
                student.current_class_id = int(class_id)
            student.save()
            messages.success(request, f'Student {student.full_name} added successfully!')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'student_mgmt/add.html', {'classes': classes})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_mgmt/detail.html', {'student': student})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    classes = Class.objects.all()
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.father_name = request.POST['father_name']
        student.father_phone = request.POST['father_phone']
        student.mother_name = request.POST['mother_name']
        student.address = request.POST['address']
        student.email = request.POST.get('email', '')
        student.phone = request.POST.get('phone', '')
        class_id = request.POST.get('current_class')
        if class_id:
            student.current_class_id = int(class_id)
        student.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_detail', pk=pk)
    return render(request, 'student_mgmt/edit.html', {'student': student, 'classes': classes})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, f'Student {student.full_name} deactivated.')
        return redirect('student_list')
    return render(request, 'student_mgmt/confirm_delete.html', {'student': student})

@login_required
def class_list(request):
    classes = Class.objects.all().prefetch_related('student_set')
    return render(request, 'student_mgmt/class_list.html', {'classes': classes})

@login_required
def class_add(request):
    from core.models import AcademicYear
    years = AcademicYear.objects.all()
    if request.method == 'POST':
        try:
            year = AcademicYear.objects.filter(is_current=True).first()
            if not year and years.exists():
                year = years.first()
            if year:
                Class.objects.create(
                    name=request.POST['name'],
                    section=request.POST['section'],
                    capacity=request.POST.get('capacity', 40),
                    room_number=request.POST.get('room_number', ''),
                    academic_year=year,
                )
                messages.success(request, 'Class added successfully!')
                return redirect('class_list')
            else:
                messages.error(request, 'Please create an Academic Year first.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'student_mgmt/class_add.html', {'years': years})


# ---- STUDENT PROMOTION ----
@login_required
def promote_students(request):
    from core.models import AcademicYear
    from django.db.models import Count
    classes = Class.objects.select_related('academic_year').annotate(student_count=Count('student'))
    next_classes = Class.objects.all()
    academic_years = AcademicYear.objects.all().order_by('-year')
    
    if request.method == 'POST':
        from_class_id = request.POST.get('from_class')
        to_class_id = request.POST.get('to_class')
        student_ids = request.POST.getlist('students')
        
        if from_class_id and to_class_id and student_ids:
            to_class = get_object_or_404(Class, pk=to_class_id)
            promoted = 0
            for sid in student_ids:
                try:
                    student = Student.objects.get(pk=sid)
                    student.current_class = to_class
                    student.save()
                    promoted += 1
                except Student.DoesNotExist:
                    pass
            messages.success(request, f'{promoted} students promoted successfully!')
            return redirect('student_list')
        else:
            messages.error(request, 'Please select class and at least one student.')
    
    selected_class_id = request.GET.get('class')
    students_in_class = []
    selected_class = None
    if selected_class_id:
        selected_class = get_object_or_404(Class, pk=selected_class_id)
        students_in_class = Student.objects.filter(current_class=selected_class, is_active=True)
    
    return render(request, 'student_mgmt/promote.html', {
        'classes': classes,
        'next_classes': next_classes,
        'students_in_class': students_in_class,
        'selected_class': selected_class,
        'academic_years': academic_years,
    })
