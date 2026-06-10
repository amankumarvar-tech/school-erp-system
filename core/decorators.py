from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def get_user_profile(user):
    try:
        return user.userprofile
    except:
        return None

def role_required(*roles):
    """Allow only specific roles"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login_view')
            profile = get_user_profile(request.user)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if not profile or profile.role not in roles:
                messages.error(request, '⛔ Access Denied! You do not have permission for this.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def permission_required(perm):
    """Allow based on permission key"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login_view')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            profile = get_user_profile(request.user)
            if not profile or not profile.can(perm):
                messages.error(request, '⛔ Access Denied! You do not have permission for this action.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def superadmin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_view')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        profile = get_user_profile(request.user)
        if not profile or profile.role != 'superadmin':
            messages.error(request, '⛔ Super Admin access required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
