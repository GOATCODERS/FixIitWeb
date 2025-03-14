from django.contrib import admin
from .models import Report, FaultType


class FaultTypeAdmin(admin.ModelAdmin):
    list_display= ('name', 'importances', 'description',)
    search_fields = ('name',)


# Customizing the admin interface for Report model
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')  # Display these fields in the list view
    search_fields = ('user__username', 'status')  # Allow searching by user or status
    list_filter = ('status',)  # Add filtering options for status
    date_hierarchy = 'created_at'  # Add date filtering


# Register models with the admin site
admin.site.register(Report, ReportAdmin)
admin.site.register(FaultType, FaultTypeAdmin)
