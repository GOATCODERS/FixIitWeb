from django.urls import path
from . import views

urlpatterns = [
    path('assign-task/<int:report_id>/', views.assign_task_view, name='assign_task'),
    path('assign-all-task/', views.assign_all_tasks, name='assign_all_tasks'),
]
