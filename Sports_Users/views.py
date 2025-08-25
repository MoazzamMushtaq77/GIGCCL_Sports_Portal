import os
import base64
from io import BytesIO
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.urls import reverse_lazy
from django.conf import settings

from django.contrib.auth import views as auth_views

from pdf2image import convert_from_path

from .forms import (
    PlayerRegistrationForm,
    PlayerLoginForm,
    PlayerProfileEditForm,
    PlayerChangePasswordForm
)
from .models import Player, CustomUser, Certificate
from sports_base.models import Notification, Team

logger = logging.getLogger(__name__)


# ---------------------- Player Auth ----------------------

def player_register(request):
    """Player registration with approval workflow."""
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Registration successful! Your account is pending approval. Please wait for admin approval.'
            )
            return redirect('Sports_Users:player_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PlayerRegistrationForm()
    return render(request, 'Sports_Users/register.html', {'form': form})


def player_login(request):
    """Custom login for players only."""
    if request.method == 'POST':
        form = PlayerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                if not user.is_player:
                    messages.error(request, 'Only players can log in here. Admins and coaches, please use the admin login.')
                    return redirect('/admin/login/')
                if user.status == 'approved' and user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('Sports_Users:player_dashboard')
                elif user.status == 'pending':
                    messages.error(request, 'Your account is pending approval. Please wait for admin approval.')
                elif user.status == 'declined':
                    messages.error(request, 'Your account has been declined. Please contact the admin.')
                else:
                    messages.error(request, 'Your account is inactive. Please contact the admin.')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    logger.error(f"Validation error in player_login for field {field}: {error}")
    else:
        form = PlayerLoginForm(request=request)
    return render(request, 'Sports_Users/login.html', {'form': form})


@login_required
def player_dashboard(request):
    """Player dashboard with notifications, team info, and certificates."""
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        messages.error(request, 'Player profile not found.')
        return redirect('Sports_Users:player_login')

    notifications = Notification.objects.filter(
        recipient=request.user, is_general=False
    ).order_by('-created_at')

    certificates = Certificate.objects.filter(player=player).order_by('-uploaded_at')

    team = player.teams.order_by('-created_at').first()
    teammates = team.players.exclude(user=request.user) if team else []

    context = {
        'player': player,
        'notifications': notifications,
        'certificates': certificates,
        'team': team,
        'teammates': teammates,
    }
    return render(request, 'Sports_Users/player_dashboard.html', context)


@login_required
def player_logout(request):
    """Log out player and redirect to login page."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('Sports_Users:player_login')


# ---------------------- Profile Views ----------------------

@login_required
def profile_view(request):
    """View player profile."""
    if not request.user.is_player or request.user.status != 'approved':
        messages.error(request, 'Access denied. Your account is not approved or you are not a player.')
        return redirect('Sports_Users:player_dashboard')

    try:
        player = request.user.player
    except Player.DoesNotExist:
        messages.error(request, 'Player profile not found.')
        return redirect('Sports_Users:player_login')

    return render(request, 'Sports_Users/profile.html', {'user': request.user, 'player': player})


@login_required
def profile_edit(request):
    """Edit player profile."""
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        messages.error(request, 'Player profile not found.')
        return redirect('Sports_Users:player_login')

    if request.method == 'POST':
        form = PlayerProfileEditForm(request.POST, request.FILES, instance=request.user, player_instance=player)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.cnic = form.cleaned_data['cnic']
            user.phone_number = form.cleaned_data['phone_number']

            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            elif request.POST.get('profile_picture_clear'):
                user.profile_picture = None

            user.save()

            player.father_name = form.cleaned_data['father_name']
            player.dob = form.cleaned_data['dob']
            player.address = form.cleaned_data['address']
            player.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('Sports_Users:profile_view')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PlayerProfileEditForm(instance=request.user, player_instance=player)

    return render(request, 'Sports_Users/profile_edit.html', {
        'form': form,
        'user': request.user,
        'player': player
    })


@login_required
def change_password(request):
    """Allow players to change password."""
    if not request.user.is_player or request.user.status != 'approved':
        messages.error(request, 'Access denied. Only approved players can change their password.')
        return redirect('Sports_Users:player_dashboard')

    if request.method == 'POST':
        form = PlayerChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            messages.success(request, 'Password changed successfully! Please log in again.')
            logout(request)
            return redirect('Sports_Users:player_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PlayerChangePasswordForm(user=request.user)

    return render(request, 'Sports_Users/change_password.html', {'form': form})


# ---------------------- Certificates ----------------------

@login_required
def certificate_view(request, certificate_id):
    """Preview a certificate (image or PDF first page)."""
    cert = get_object_or_404(Certificate, id=certificate_id, player__user=request.user)
    file_path = cert.certificate_file.path
    file_url = cert.certificate_file.url
    ext = os.path.splitext(file_path)[1].lower()

    cert_image_url = None
    if ext == ".pdf":
        try:
            images = convert_from_path(
                file_path,
                first_page=1,
                last_page=1,
                poppler_path=settings.POPPLER_PATH
            )
            buf = BytesIO()
            images[0].save(buf, format="PNG")
            buf.seek(0)
            cert_image_url = "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"PDF Conversion Error: {e}")
            cert_image_url = None
    else:
        cert_image_url = file_url

    return render(request, "Sports_Users/certificate_view.html", {
        "certificate": cert,
        "cert_image_url": cert_image_url,
        "file_url": file_url,
    })


@login_required
def download_certificate(request, certificate_id):
    """Download certificate file."""
    cert = get_object_or_404(Certificate, id=certificate_id, player__user=request.user)
    file_path = cert.certificate_file.path
    file_name = os.path.basename(file_path)
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename=file_name)


# ---------------------- Password Reset (fixed) ----------------------

class CustomPasswordResetView(auth_views.PasswordResetView):
    """
    Use local DOMAIN/PROTOCOL in the email so links match your dev server exactly.
    """
    def get_email_context(self, context):
        context = super().get_email_context(context)
        # These must be set in settings.py (see notes below)
        context["domain"] = getattr(settings, "DOMAIN", "127.0.0.1:8000")
        context["protocol"] = getattr(settings, "PROTOCOL", "http")
        return context


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    Rely on Django's built-in token/UID validation.
    We only add a success message + redirect to login.
    """
    template_name = "Sports_Users/password_reset_confirm.html"
    success_url = reverse_lazy("Sports_Users:player_login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password has been reset successfully. Please log in.")
        return response
