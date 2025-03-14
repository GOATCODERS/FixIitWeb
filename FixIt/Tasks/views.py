from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from reports.models import Report
from .models import Task
from authentication.models import Technician
from .tasks import create_task, assign_tasks
from authentication.decorators import role_required


def assign_task_view(request, report_id):
    """Assigns a task to an available technician and redirects to the task details."""
    print(" [Passed here 2] +++++++++++++")
    report = get_object_or_404(Report, id=report_id, status="Pending")
    technician = Technician.objects.filter(is_available=True).first()

    if not technician:
        messages.error(request, "No available technicians at the moment.")
        return redirect("report_detail", report_id=report_id)
    print(f"{technician.count}technician are available, proceeding to ")
    task = create_task(report, technician)

    messages.success(request, f"{task} successfully assigned to {technician.user.username}.")
    return redirect("report_detail", report_id=report_id)

@role_required(['admin'])
def assign_all_tasks(request):
    assign_tasks.delay()
    return redirect("list_reports")

