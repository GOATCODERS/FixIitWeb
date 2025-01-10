from django.db import models
from django.conf import settings
from reports.models import Report

class Appointment(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='appointment')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_appointments')
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resident_appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Scheduled', 'Scheduled'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Scheduled'
    )

    def __str__(self):
        return f"Appointment for Report {self.report.id} on {self.date} at {self.time}"
