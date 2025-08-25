from django.urls import path
from . import views

app_name = 'Sports_Users'

urlpatterns = [
    # Auth
    path('register/', views.player_register, name='player_register'),
    path('login/', views.player_login, name='player_login'),
    path('logout/', views.player_logout, name='player_logout'),

    # Dashboard & Profile
    path('dashboard/', views.player_dashboard, name='player_dashboard'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('change-password/', views.change_password, name='change_password'),

    # Certificates
    path('certificate/<int:certificate_id>/', views.certificate_view, name='certificate_view'),
    path('certificate/<int:certificate_id>/download/', views.download_certificate, name='download_certificate'),

    # Password reset (send email)
    path(
        'password_reset/',
        views.CustomPasswordResetView.as_view(
            template_name='Sports_Users/password_reset_form.html',
            email_template_name='Sports_Users/password_reset_email.html',
            subject_template_name='Sports_Users/password_reset_subject.txt',
            success_url='/Sports_Users/login/?email_sent=true',
        ),
        name='password_reset',
    ),

    # Email link → confirm page (set new password)
    path(
        'reset/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
]
