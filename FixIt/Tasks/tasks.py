from celery import shared_task
from django.db import transaction
from reports.models import Report
from .models import Task
from authentication.models import Technician
import logging

logger = logging.getLogger(__name__)


@shared_task
def assign_tasks():
    unassigned_reports = Report.objects.filter(status="Pending").order_by('created_at')
    available_technicians = Technician.objects.filter(is_available=True)

    if not available_technicians.exists():
        logger.info("No available technicians.")
        return "No available technicians."

    if not unassigned_reports.exists():
        logger.info("No unassigned reports.")
        return "No unassigned reports."

    assigned_count = 0

    for report in unassigned_reports:
        with transaction.atomic():  # Ensure a technician isn't double-assigned
            technician = Technician.objects.select_for_update(skip_locked=True).filter(is_available=True).first()
            if not technician:
                logger.info("All available technicians have been assigned.")
                break

            try:
                create_task(report, technician)
                assigned_count += 1
            except Exception as e:
                logger.error(f"Failed to assign task for report {report.id}: {str(e)}")

    return f"Assigned {assigned_count} tasks."


def create_task(report, technician):
    """Creates a task and updates associated records."""
    new_task = Task.objects.create(report=report, technician=technician, status="In Progress")

    # Update report and technician status
    report.status = "In Progress"
    report.save(update_fields=["status"])

    technician.is_available = False
    technician.save(update_fields=["is_available"])

    logger.info(f'Task {new_task.id} created for Report {report.id}, assigned to Technician {technician.id}.')
    return f'Task {new_task.id} created.'
