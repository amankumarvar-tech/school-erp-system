from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import StudentAttendance, TeacherAttendance
from student_mgmt.models import Student, Class

@login_required
def attendance_list(request):
    today = timezone.now().date()
    date = request.GET.get('date', str(today))
    class_id = request.GET.get('class_id')
    classes = Class.objects.all()
    attendance = StudentAttendance.objects.filter(date=date).select_related('student', 'class_name')
    if class_id:
        attendance = attendance.filter(class_name_id=class_id)
    return render(request, 'attendance_mgmt/list.html', {
        'attendance': attendance, 'date': date, 'classes': classes, 'class_id': class_id
    })

@login_required
def mark_attendance(request):
    classes = Class.objects.all()
    today = timezone.now().date()
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        date = request.POST.get('date', str(today))
        students = Student.objects.filter(current_class_id=class_id, is_active=True)
        count = 0
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            StudentAttendance.objects.update_or_create(
                student=student, date=date,
                defaults={'status': status, 'class_name_id': class_id}
            )
            count += 1
        messages.success(request, f'Attendance marked for {count} students!')
        return redirect('attendance_list')
    
    class_id = request.GET.get('class_id')
    students = []
    if class_id:
        students = Student.objects.filter(current_class_id=class_id, is_active=True)
    return render(request, 'attendance_mgmt/mark.html', {
        'classes': classes, 'students': students, 'class_id': class_id, 'today': today
    })
