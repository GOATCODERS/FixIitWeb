from django.urls import path
from . import views
from .views import ReportUpdateView


urlpatterns = [
    path('report/', views.report_fault, name='report_fault'),
    path('report/list/', views.list_reports, name='list_reports'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    # path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('report/<int:pk>/update/', ReportUpdateView.as_view(), name='report_update'),
    path('report/my-view-url/', views.my_view, name='my_view_url'),
    path('employee/dashboard/', views.employee_dashboard_view, name='employee_dashboard_view'),
]
