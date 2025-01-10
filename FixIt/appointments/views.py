from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from reports.models import Report

@login_required
def schedule_appointment(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.report = report
            appointment.employee = request.user  # Assuming employee is scheduling
            appointment.resident = report.submitted_by
            appointment.save()
            return redirect('report_detail', report_id=report.id)
    else:
        form = AppointmentForm()
    return render(request, 'appointments/schedule.html', {'form': form, 'report': report})

@login_required
def appointment_list(request):
    if request.user.is_staff:  # Employee/Admin view
        appointments = Appointment.objects.filter(employee=request.user)
    else:  # Resident view
        appointments = Appointment.objects.filter(resident=request.user)
    return render(request, 'appointments/list.html', {'appointments': appointments})
