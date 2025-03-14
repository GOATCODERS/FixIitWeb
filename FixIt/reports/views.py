# reports/views.py
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReportForm
from .models import Report
from Tasks.models import Task
from authentication.models import Technician
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()


@login_required
def report_fault(request):
    if request.user.is_staff:
        reports = Report.objects.order_by('-created_at')
    else:
        reports = Report.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)  # Don't save to the database yet
            report.user = request.user  # Assign the logged-in user to the report
            report.save()  # Save the report with the user field populated
            messages.success(request, "Your fault report has been submitted successfully!")
            return redirect('list_reports')  # Redirect to the list of reports
        else:
            messages.error(request, f"Something went wrong while submitting the form {form.errors}")
    else:
        form = ReportForm()
    return render(request, 'reporting/report.html', {'form': form, 'reports': reports})


@login_required
def list_reports(request):
    current_user = request.user
    print("your is staff: ", current_user.is_staff)

    if current_user.role == 'employee':
        reports = Report.objects.filter(
            Q(status='Pending') | Q(task__technician__user=request.user))\
            .distinct().order_by('-created_at')
        return render(request, 'reporting/admin_dashboard.html', {'reports': reports})
    elif current_user.is_staff:
        reports = Report.objects.order_by('-created_at')
        return render(request, 'reporting/admin_dashboard.html', {'reports': reports})
    else:
        reports = Report.objects.filter(user=current_user).order_by('-created_at')
    return render(request, 'reporting/list_reports.html', {'reports': reports})


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    print(f'User role: {request.user.role}')

    if request.user.role == 'employee':
        reports = Report.objects.filter(
            Q(status='Pending') | Q(task__technician__user=request.user)
        ).distinct().order_by('-created_at')

        print(f'Retrieved reports for employee: {reports}')  # Debugging line
    elif request.user.is_staff:
        reports = Report.objects.order_by('-created_at')
    else:
        reports = Report.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'reporting/report_detail.html', {'report': report, 'reports': reports})


class ReportUpdateView(UpdateView):
    model = Report
    fields = ['photo', 'description']  # Fields the user can update
    template_name = 'reporting/report_update.html'  # Path to the update template
    success_url = reverse_lazy('list_reports')  # Redirect to the report list after update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update Report #{self.object.id}'
        return context


@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON body
        name = data.get('name')
        age = data.get('age')

        # Process data and return a response
        return JsonResponse({'status': 'success', 'name': name + " " + str(age), 'age': age})


def employee_dashboard_view(request):
    technician = get_object_or_404(Technician, user=request.user)  # Get Technician linked to the logged-in user
    tasks = Task.objects.filter(technician=technician).order_by('-created_at')  # QuerySet of tasks

    report = None
    task = None

    for task in tasks:
        if task.status == "In Progress":
            report = task.report
            break  # Only take the first "In Progress" task

    return render(request, 'employee/dashboard.html', {
        'report': report,
        'task': task,
        'tasks': tasks
    })
