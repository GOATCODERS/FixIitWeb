from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-technician', views.add_technician, name='add_technician'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),
    path('employee/dashboard', views.employee_dashboard, name='employee_dashboard'),
    path("profile/", views.profile_view, name="profile"),
]
