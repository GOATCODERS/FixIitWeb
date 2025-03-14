from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class FaultType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    importances = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fault_type = models.ForeignKey(FaultType, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='reports/photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report #{self.id} - {self.fault_type}"

