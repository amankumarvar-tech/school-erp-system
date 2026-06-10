from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from .decorators import superadmin_required, get_user_profile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password. Please try again.'})
    return render(request, 'login.html', {})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required
def dashboard(request):
    from student_mgmt.models import Student, Class
    from teacher_mgmt.models import Teacher
    from fees_mgmt.models import FeePayment
    from attendance_mgmt.models import StudentAttendance
    from communication_mgmt.models import Notice
    from exam_mgmt.models import Exam

    today = timezone.now().date()
    profile = get_user_profile(request.user)

    stats = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
        'total_classes': Class.objects.count(),
        'fees_collected': FeePayment.objects.filter(status='paid').aggregate(total=Sum('amount_paid'))['total'] or 0,
        'fees_pending': FeePayment.objects.filter(status__in=['pending','overdue']).count(),
        'today_attendance': StudentAttendance.objects.filter(date=today, status='present').count(),
        'active_notices': Notice.objects.filter(is_active=True).count(),
        'upcoming_exams': Exam.objects.filter(exam_date__gte=today).count(),
    }

    recent_students = Student.objects.order_by('-created_at')[:5]
    active_notices = Notice.objects.filter(is_active=True).order_by('-published_at')[:5]
    upcoming_exams = Exam.objects.filter(exam_date__gte=today).order_by('exam_date')[:5]
    overdue_fees = FeePayment.objects.filter(status='overdue').select_related('student').order_by('due_date')[:5]

    return render(request, 'dashboard.html', {
        'stats': stats,
        'recent_students': recent_students,
        'active_notices': active_notices,
        'upcoming_exams': upcoming_exams,
        'overdue_fees': overdue_fees,
        'today': today,
        'user_profile': profile,
    })

@login_required
def settings_view(request):
    from .models import SchoolProfile, AcademicYear
    profile = get_user_profile(request.user)
    if profile and profile.role == 'staff':
        messages.error(request, '⛔ Access Denied!')
        return redirect('dashboard')

    school = SchoolProfile.objects.first()
    years = AcademicYear.objects.all().order_by('-year')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'profile' and school:
            school.name = request.POST.get('name', school.name)
            school.address = request.POST.get('address', school.address)
            school.phone = request.POST.get('phone', school.phone)
            school.email = request.POST.get('email', school.email)
            school.principal_name = request.POST.get('principal_name', school.principal_name)
            school.board = request.POST.get('board', school.board)
            school.save()
            messages.success(request, 'School profile updated!')
            return redirect('settings_view')
        elif action == 'add_year':
            try:
                AcademicYear.objects.create(
                    year=request.POST['year'],
                    start_date=request.POST['start_date'],
                    end_date=request.POST['end_date'],
                    is_current=request.POST.get('is_current') == 'on'
                )
                messages.success(request, 'Academic year added!')
            except Exception as e:
                messages.error(request, f'Error: {e}')
            return redirect('settings_view')
    return render(request, 'core/settings.html', {'profile': school, 'years': years})

# ============ USER MANAGEMENT (SuperAdmin only) ============

@superadmin_required
def user_list(request):
    from .models import UserProfile
    users = User.objects.select_related('userprofile').order_by('-date_joined')
    return render(request, 'core/user_list.html', {'users': users})

@superadmin_required
def user_add(request):
    from .models import UserProfile
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'staff')
        phone = request.POST.get('phone', '')
        department = request.POST.get('department', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists.')
            return render(request, 'core/user_add.html')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        if role == 'superadmin':
            user.is_staff = True
            user.save()

        UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone,
            department=department,
        )
        messages.success(request, f'✅ User "{username}" created with role {role}!')
        return redirect('user_list')
    return render(request, 'core/user_add.html')

@superadmin_required
def user_edit(request, pk):
    from .models import UserProfile
    user = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': 'staff'})

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        new_pass = request.POST.get('password', '').strip()
        if new_pass:
            user.set_password(new_pass)
        user.save()

        profile.role = request.POST.get('role', profile.role)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.department = request.POST.get('department', profile.department)
        profile.is_active = request.POST.get('is_active') == 'on'
        profile.save()

        if profile.role == 'superadmin':
            user.is_staff = True
            user.save()

        messages.success(request, f'✅ User "{user.username}" updated!')
        return redirect('user_list')

    return render(request, 'core/user_edit.html', {'edit_user': user, 'profile': profile})

@superadmin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, 'Aap apna khud ka account delete nahi kar sakte!')
        return redirect('user_list')
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted.')
    return redirect('user_list')
