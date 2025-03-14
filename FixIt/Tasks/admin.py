from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('report', 'technician', 'status', 'created_at', 'updated_at')  # Show timestamps in list
    search_fields = ('report__fault_type', 'status')  # Search by report's fault type
    list_filter = ('status', 'technician')  # Filter by status and technician
    ordering = ('-created_at',)  # Show latest tasks first


admin.site.register(Task, TaskAdmin)
