from django.db import models
from student_mgmt.models import Student

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[('boys','Boys'),('girls','Girls'),('mixed','Mixed')])
    warden_name = models.CharField(max_length=100)
    warden_phone = models.CharField(max_length=15)
    total_rooms = models.IntegerField()
    address = models.TextField(blank=True)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    def __str__(self): return self.name

class HostelRoom(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    floor = models.IntegerField(default=1)
    capacity = models.IntegerField(default=4)
    room_type = models.CharField(max_length=20, choices=[('single','Single'),('double','Double'),('triple','Triple'),('dormitory','Dormitory')], default='double')
    has_ac = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    def __str__(self): return f"{self.hostel.name} - Room {self.room_number}"
    @property
    def occupancy(self): return self.allocations.filter(is_active=True).count()
    @property
    def is_full(self): return self.occupancy >= self.capacity

class HostelAllocation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='hostel_alloc')
    room = models.ForeignKey(HostelRoom, on_delete=models.CASCADE, related_name='allocations')
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    def __str__(self): return f"{self.student.full_name} - {self.room}"
