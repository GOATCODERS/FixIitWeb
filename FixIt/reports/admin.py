from django.contrib import admin
from .models import Report, Technician

# Customizing the admin interface for Report model
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')  # Display these fields in the list view
    search_fields = ('user__username', 'status')  # Allow searching by user or status
    list_filter = ('status',)  # Add filtering options for status
    date_hierarchy = 'created_at'  # Add date filtering

# Customizing the admin interface for Technician model
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'is_available')  # Display relevant fields
    search_fields = ('user__username', 'expertise')  # Allow searching by technician username or expertise

    # Example of adding a custom method to display in the list view
    def assigned_reports(self, obj):
        return obj.report_set.count()  # Display the count of reports assigned to the technician
    assigned_reports.short_description = 'Assigned Reports'

# Register models with the admin site
admin.site.register(Report, ReportAdmin)
admin.site.register(Technician, TechnicianAdmin)
