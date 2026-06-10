#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
from core.models import UserProfile

# Create Super Admin
if not User.objects.filter(username='superadmin').exists():
    u = User.objects.create_superuser('superadmin', 'superadmin@school.com', 'Admin@1234')
    UserProfile.objects.create(user=u, role='superadmin', department='Management')
    print('SuperAdmin created: superadmin / Admin@1234')

# Create Admin
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_user('admin', 'admin@school.com', 'Admin@1234')
    u.is_staff = False
    u.save()
    UserProfile.objects.create(user=u, role='admin', department='Administration')
    print('Admin created: admin / Admin@1234')

# Create Staff
if not User.objects.filter(username='staff').exists():
    u = User.objects.create_user('staff', 'staff@school.com', 'Staff@1234')
    UserProfile.objects.create(user=u, role='staff', department='Teaching')
    print('Staff created: staff / Staff@1234')
"
