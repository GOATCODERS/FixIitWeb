# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """Adds a CSS class to a form field."""
    return field.as_widget(attrs={"class": css_class})


@register.filter
def status_color(status):
    """Maps report statuses to colors."""
    colors = {
        'Pending': 'warning',       # Yellow
        'In Progress': 'primary',  # Blue
        'Resolved': 'success',     # Green
        'Rejected': 'danger',     # Green
    }
    return colors.get(status, 'secondary')  # Default to gray