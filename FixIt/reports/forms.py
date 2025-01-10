from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['fault_type', 'location', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 3,
                'placeholder': 'Describe the issue in detail...',
            }),
            'fault_type': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'location': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'photo': forms.FileInput(attrs={'class': 'form-control rounded-pill'}),
        }

