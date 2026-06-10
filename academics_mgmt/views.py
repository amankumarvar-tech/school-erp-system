from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject, Timetable
from student_mgmt.models import Class

@login_required
def timetable_list(request):
    class_id = request.GET.get('class_id')
    classes = Class.objects.all()
    timetable = []
    if class_id:
        timetable = Timetable.objects.filter(class_name_id=class_id).order_by('day', 'period_number')
    return render(request, 'academics_mgmt/timetable.html', {'timetable': timetable, 'classes': classes, 'class_id': class_id})
