from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,  Technician


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    # Fields for the user creation form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff'),
        }),
    )
    # You can override the methods for user creation here as well if needed.


class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'is_available')  # Display relevant fields
    search_fields = ('user__username', 'expertise')  # Allow searching by technician username or expertise

    # Example of adding a custom method to display in the list view
    def assigned_reports(self, obj):
        return obj.report_set.count()  # Display the count of reports assigned to the technician
    assigned_reports.short_description = 'Assigned Reports'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Technician, TechnicianAdmin)

