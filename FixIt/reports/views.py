# reports/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReportForm
from .models import Report
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def report_fault(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)  # Don't save to the database yet
            report.user = request.user  # Assign the logged-in user to the report
            report.save()  # Save the report with the user field populated
            messages.success(request, "Your fault report has been submitted successfully!")
            return redirect('list_reports')  # Redirect to the list of reports
    else:
        form = ReportForm()
    return render(request, 'reporting/report.html', {'form': form})


@login_required
def list_reports(request):
    if request.user.is_staff:
        userIsStaff = request.user.is_staff
        print("your is staff: ", userIsStaff)
        reports = Report.objects.order_by('-created_at')
        return render(request, 'reporting/admin_dashboard.html', {'reports': reports})

    else:
        reports = Report.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reporting/list_reports.html', {'reports': reports})

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'reporting/report_detail.html', {'report': report})
    