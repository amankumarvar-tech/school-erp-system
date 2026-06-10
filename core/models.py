from django.db import models
from django.contrib.auth.models import User

class SchoolProfile(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='school/', blank=True)
    established_year = models.IntegerField()
    principal_name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, blank=True)
    board = models.CharField(max_length=50, choices=[
        ('CBSE', 'CBSE'), ('ICSE', 'ICSE'), ('STATE', 'State Board'), ('IB', 'IB')
    ])
    def __str__(self):
        return self.name

class AcademicYear(models.Model):
    year = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    def __str__(self):
        return self.year
    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]

    # Role-based permissions mapping
    ROLE_PERMISSIONS = {
        'superadmin': {
            'label': 'Super Admin',
            'color': '#7c3aed',
            'badge': 'badge-purple',
            'icon': 'fa-crown',
            'can_manage_users': True,
            'can_manage_roles': True,
            'can_delete_data': True,
            'can_manage_fees': True,
            'can_manage_payroll': True,
            'can_view_reports': True,
            'can_manage_students': True,
            'can_manage_teachers': True,
            'can_manage_attendance': True,
            'can_manage_exams': True,
            'can_manage_library': True,
            'can_manage_hostel': True,
            'can_manage_transport': True,
            'can_manage_settings': True,
            'can_excel_import': True,
        },
        'admin': {
            'label': 'Admin',
            'color': '#2563eb',
            'badge': 'badge-info',
            'icon': 'fa-user-shield',
            'can_manage_users': False,
            'can_manage_roles': False,
            'can_delete_data': False,
            'can_manage_fees': True,
            'can_manage_payroll': True,
            'can_view_reports': True,
            'can_manage_students': True,
            'can_manage_teachers': True,
            'can_manage_attendance': True,
            'can_manage_exams': True,
            'can_manage_library': True,
            'can_manage_hostel': True,
            'can_manage_transport': True,
            'can_manage_settings': False,
            'can_excel_import': True,
        },
        'staff': {
            'label': 'Staff',
            'color': '#059669',
            'badge': 'badge-success',
            'icon': 'fa-user',
            'can_manage_users': False,
            'can_manage_roles': False,
            'can_delete_data': False,
            'can_manage_fees': False,
            'can_manage_payroll': False,
            'can_view_reports': False,
            'can_manage_students': True,
            'can_manage_teachers': False,
            'can_manage_attendance': True,
            'can_manage_exams': True,
            'can_manage_library': True,
            'can_manage_hostel': False,
            'can_manage_transport': False,
            'can_manage_settings': False,
            'can_excel_import': False,
        },
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True)
    address = models.TextField(blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.get_role_display()}"

    def get_permissions(self):
        return self.ROLE_PERMISSIONS.get(self.role, self.ROLE_PERMISSIONS['staff'])

    def can(self, perm):
        return self.get_permissions().get(perm, False)

    def role_color(self):
        return self.ROLE_PERMISSIONS.get(self.role, {}).get('color', '#6b7280')

    def role_icon(self):
        return self.ROLE_PERMISSIONS.get(self.role, {}).get('icon', 'fa-user')
