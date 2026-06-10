from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, ExamResult, ExamType
from student_mgmt.models import Class, Student
from academics_mgmt.models import Subject

@login_required
def exam_list(request):
    exams = Exam.objects.select_related('exam_type','class_name','subject').order_by('exam_date')
    return render(request, 'exam_mgmt/list.html', {'exams': exams})

@login_required
def exam_add(request):
    exam_types = ExamType.objects.all()
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            Exam.objects.create(
                exam_type_id=request.POST['exam_type'],
                class_name_id=request.POST['class_name'],
                subject_id=request.POST['subject'],
                exam_date=request.POST['exam_date'],
                start_time=request.POST['start_time'],
                end_time=request.POST['end_time'],
                max_marks=request.POST['max_marks'],
                pass_marks=request.POST['pass_marks'],
                venue=request.POST.get('venue', ''),
            )
            messages.success(request, 'Exam scheduled successfully!')
            return redirect('exam_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'exam_mgmt/add.html', {'exam_types': exam_types, 'classes': classes, 'subjects': subjects})

@login_required
def result_entry(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    students = Student.objects.filter(current_class=exam.class_name, is_active=True)
    if request.method == 'POST':
        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            if marks:
                ExamResult.objects.update_or_create(
                    exam=exam, student=student,
                    defaults={'marks_obtained': marks, 'is_absent': False}
                )
        messages.success(request, 'Results saved successfully!')
        return redirect('exam_list')
    existing = {r.student_id: r for r in ExamResult.objects.filter(exam=exam)}
    return render(request, 'exam_mgmt/result_entry.html', {'exam': exam, 'students': students, 'existing': existing})
