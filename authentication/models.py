from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('Service1', 'Service 1'),
        ('Service2', 'Service 2'),
        ('Service3', 'Service 3'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    service_required = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_required} on {self.appointment_date} at {self.appointment_time}"
