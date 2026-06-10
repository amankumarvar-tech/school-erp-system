from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BusRoute, StudentTransport
from student_mgmt.models import Student

@login_required
def transport_dashboard(request):
    routes = BusRoute.objects.filter(is_active=True).annotate_with_counts() if hasattr(BusRoute.objects, 'annotate_with_counts') else BusRoute.objects.filter(is_active=True)
    from django.db.models import Count
    routes = BusRoute.objects.filter(is_active=True).annotate(student_count=Count('students'))
    total_students = StudentTransport.objects.filter(is_active=True).count()
    return render(request, 'transport_mgmt/dashboard.html', {'routes': routes, 'total_students': total_students})

@login_required
def route_add(request):
    if request.method == 'POST':
        try:
            BusRoute.objects.create(
                route_name=request.POST['route_name'],
                route_number=request.POST['route_number'],
                start_point=request.POST['start_point'],
                end_point=request.POST['end_point'],
                stops=request.POST.get('stops',''),
                driver_name=request.POST['driver_name'],
                driver_phone=request.POST['driver_phone'],
                vehicle_number=request.POST['vehicle_number'],
                capacity=request.POST.get('capacity',40),
                morning_departure=request.POST['morning_departure'],
                evening_departure=request.POST['evening_departure'],
                monthly_fee=request.POST.get('monthly_fee',0),
                distance_km=request.POST.get('distance_km',0),
            )
            messages.success(request, 'Route added!')
            return redirect('transport_dashboard')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'transport_mgmt/route_add.html')

@login_required
def assign_transport(request):
    routes = BusRoute.objects.filter(is_active=True)
    students = Student.objects.filter(is_active=True).exclude(transport__isnull=False)
    if request.method == 'POST':
        try:
            StudentTransport.objects.create(
                student_id=request.POST['student'],
                route_id=request.POST['route'],
                pickup_stop=request.POST['pickup_stop'],
                drop_stop=request.POST.get('drop_stop',''),
                start_date=request.POST['start_date'],
            )
            messages.success(request, 'Transport assigned!')
            return redirect('transport_dashboard')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'transport_mgmt/assign.html', {'routes': routes, 'students': students})
