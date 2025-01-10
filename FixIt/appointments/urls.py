from django.urls import path
from . import views

urlpatterns = [
    path('schedule/<int:report_id>/', views.schedule_appointment, name='schedule_appointment'),
    path('list/', views.appointment_list, name='appointment_list'),
]
