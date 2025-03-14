from django.db import models
from reports.models import Report
from authentication.models import Technician
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('paused', 'Paused'),
        ('failed', 'Failed'),
        ('complete', 'Complete'),
    ]

    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(null=True, blank=True)  # Optional rating field

    def __str__(self):
        return f"Task #{self.id} - {self.report.fault_type}"
