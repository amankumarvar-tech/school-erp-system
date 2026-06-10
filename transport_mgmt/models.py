from django.db import models
from student_mgmt.models import Student

class BusRoute(models.Model):
    route_name = models.CharField(max_length=100)
    route_number = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    stops = models.TextField(help_text="Comma separated stop names")
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    conductor_name = models.CharField(max_length=100, blank=True)
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50, blank=True)
    capacity = models.IntegerField(default=40)
    morning_departure = models.TimeField()
    evening_departure = models.TimeField()
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"Route {self.route_number} - {self.route_name}"

class StudentTransport(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='transport')
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='students')
    pickup_stop = models.CharField(max_length=100)
    drop_stop = models.CharField(max_length=100)
    pickup_time = models.TimeField(null=True, blank=True)
    drop_time = models.TimeField(null=True, blank=True)
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    def __str__(self): return f"{self.student.full_name} - {self.route}"
