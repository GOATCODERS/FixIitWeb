from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Technician

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['user', 'expertise', 'is_available']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'btn-check', 'id': 'btn-check-4'}),
        }