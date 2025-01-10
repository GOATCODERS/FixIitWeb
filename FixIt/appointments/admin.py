from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('report', 'employee', 'resident', 'date', 'time', 'status')
    search_fields = ('report__id', 'employee__username', 'resident__username', 'status')
    list_filter = ('status', 'date')

admin.site.register(Appointment, AppointmentAdmin)
