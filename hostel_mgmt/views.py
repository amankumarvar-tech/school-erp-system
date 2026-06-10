from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Hostel, HostelRoom, HostelAllocation
from student_mgmt.models import Student

@login_required
def hostel_dashboard(request):
    hostels = Hostel.objects.all()
    total_rooms = HostelRoom.objects.count()
    occupied = HostelAllocation.objects.filter(is_active=True).count()
    available_rooms = HostelRoom.objects.filter(is_available=True)
    recent = HostelAllocation.objects.filter(is_active=True).select_related('student','room','room__hostel')[:10]
    return render(request, 'hostel_mgmt/dashboard.html', {
        'hostels': hostels, 'total_rooms': total_rooms,
        'occupied': occupied, 'recent': recent,
    })

@login_required
def hostel_add(request):
    if request.method == 'POST':
        Hostel.objects.create(
            name=request.POST['name'], type=request.POST['type'],
            warden_name=request.POST['warden_name'], warden_phone=request.POST['warden_phone'],
            total_rooms=request.POST['total_rooms'], monthly_fee=request.POST.get('monthly_fee',0)
        )
        messages.success(request, 'Hostel added!')
        return redirect('hostel_dashboard')
    return render(request, 'hostel_mgmt/hostel_add.html')

@login_required
def room_add(request):
    hostels = Hostel.objects.all()
    if request.method == 'POST':
        HostelRoom.objects.create(
            hostel_id=request.POST['hostel'], room_number=request.POST['room_number'],
            floor=request.POST.get('floor',1), capacity=request.POST.get('capacity',4),
            room_type=request.POST.get('room_type','double'),
        )
        messages.success(request, 'Room added!')
        return redirect('hostel_dashboard')
    return render(request, 'hostel_mgmt/room_add.html', {'hostels': hostels})

@login_required
def allocate_room(request):
    rooms = HostelRoom.objects.filter(is_available=True).select_related('hostel')
    students = Student.objects.filter(is_active=True).exclude(hostel_alloc__is_active=True)
    if request.method == 'POST':
        try:
            HostelAllocation.objects.create(
                student_id=request.POST['student'],
                room_id=request.POST['room'],
                check_in=request.POST['check_in'],
            )
            messages.success(request, 'Room allocated!')
            return redirect('hostel_dashboard')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'hostel_mgmt/allocate.html', {'rooms': rooms, 'students': students})
