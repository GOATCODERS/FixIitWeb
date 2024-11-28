from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_fault, name='report_fault'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
]
