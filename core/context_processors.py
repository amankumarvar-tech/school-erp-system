def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            return {
                'user_profile': profile,
                'user_role': profile.role,
                'user_permissions': profile.get_permissions(),
                'is_superadmin': profile.role == 'superadmin' or request.user.is_superuser,
                'is_admin': profile.role in ['superadmin', 'admin'] or request.user.is_superuser,
                'is_staff_role': profile.role == 'staff',
            }
        except:
            pass
    return {
        'user_profile': None,
        'user_role': None,
        'user_permissions': {},
        'is_superadmin': request.user.is_superuser if request.user.is_authenticated else False,
        'is_admin': request.user.is_superuser if request.user.is_authenticated else False,
        'is_staff_role': False,
    }
