from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import CustomUserCreationForm, TechnicianForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from authentication.decorators import role_required
from django.contrib.sites.shortcuts import get_current_site
from .models import Technician

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.role == 'employee':
                user.is_staff = True  # Required for admin users
            if user.role == 'admin':
                user.is_staff = True  # Required for admin users
                user.is_superuser = True  # Make the user a superuser
            user.save()
            messages.success(request, 'New user account created successfully')
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login Successful')
            # Redirect based on user role
            if user.role == 'resident':
                return redirect('home')
            elif user.role == 'employee':
                return redirect('employee_dashboard')
            elif user.role == 'admin':
                return redirect('/admin/')  # Replace with your URL for admin
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                # Get email
                email = form.cleaned_data['email']
                associated_users = User.objects.filter(email=email)
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "authentication/password_reset_email.html"
                        c = {
                            "email": user.email,
                            'domain': get_current_site(request).domain,
                            'site_name': 'BidnessVille',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'https' if request.is_secure() else 'http'
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            msg = EmailMessage(subject, email, to=[user.email])
                            msg.send()
                        except Exception as e:
                            # Log the error (in production, use proper logging)
                            print(f"Error sending email: {e}")
                            messages.error(request, "Error sending email. Please try again later.")
                            return render(request, "authentication/password_reset.html", {"form": form})
                        return redirect("password_reset_done")
                else:
                    # Return to same page but don't reveal that email doesn't exist
                    return redirect("password_reset_done")
            except Exception as e:
                messages.error(request, "An error occurred. Please try again.")
                print(f' Error: {e}')
                return render(request, "authentication/password_reset.html", {"form": form})
    else:
        form = PasswordResetForm()
    return render(request, "authentication/password_reset.html", {"form": form})

def password_reset_done(request):
    return render(request, 'authentication/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, "authentication/password_reset_confirm.html", {"form": form})
    else:
        return render(request, "authentication/password_reset_invalid.html")

def password_reset_complete(request):
    return render(request, "authentication/password_reset_complete.html")

@role_required(['admin', 'employee'])
def employee_dashboard(request):
    return redirect('employee_dashboard_view')

def home(request):
    return render(request, 'homepage.html')


def add_technician(request):
    technicians = Technician.objects.order_by('user')
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            technician = form.save(commit=False)
            technician.save()
            messages.success(request, 'Technician successfully added')
            return redirect('list_reports')
        else:
            messages.error(request, 'Something went wrong')

    else:
        form = TechnicianForm()
    return render(request, 'authentication/add_technician.html', {'form': form, 'technicians': technicians})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        # Update First Name and Last Name
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Profile updated successfully!")

        # Update Technician Availability (if applicable)
        if user.is_staff:
            if hasattr(user, "technician"):
                is_available = request.POST.get("is_available") == "True"
                user.technician.is_available = is_available
                user.technician.save()
                messages.success(request, "Availability updated successfully!")

        return redirect("profile")  # Prevent resubmission on refresh

    return render(request, "profiles/profile.html", {"user": user})