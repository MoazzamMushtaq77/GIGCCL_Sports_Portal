from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Player, Certificate

class CustomUserAdminForm(forms.ModelForm):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the current password.")
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False, help_text="Must match the new password.")

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'cnic', 'phone_number', 'profile_picture', 'is_coach', 'is_player', 'status', 'is_staff', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password or confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match.")
            if new_password:
                cleaned_data["password"] = make_password(new_password)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.password = make_password(new_password)
        if commit:
            user.save()
        return user

class PlayerAdminForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(is_player=True)

class CertificateAdminForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.all()

class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'cnic', 'phone_number', 'is_coach', 'is_player', 'status', 'is_superuser']
    list_filter = ['is_coach', 'is_player', 'status', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'new_password', 'confirm_password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'cnic', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Additional Information', {'fields': ('is_coach', 'is_player', 'status')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'cnic', 'phone_number', 'profile_picture', 'is_coach', 'is_player', 'status', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ['email', 'first_name', 'last_name', 'cnic']
    ordering = ['email']
    actions = ['approve_users', 'decline_users']

    def get_coach_profile(self, obj):
        return obj.coach_profile.name if hasattr(obj, 'coach_profile') else '-'
    get_coach_profile.short_description = 'Coach Profile'

    def approve_users(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected users have been approved.")

    def decline_users(self, request, queryset):
        queryset.update(status='declined')
        self.message_user(request, "Selected users have been declined.")

class PlayerAdmin(admin.ModelAdmin):
    form = PlayerAdminForm
    list_display = ['user', 'father_name', 'sport', 'college_roll_no', 'blood_group', 'disability']
    search_fields = ['user__email', 'father_name', 'college_roll_no']
    list_filter = ['sport', 'blood_group', 'disability']

class CertificateAdmin(admin.ModelAdmin):
    form = CertificateAdminForm
    list_display = ['title', 'player', 'uploaded_at']
    list_filter = ['uploaded_at', 'player']
    search_fields = ['title', 'player__user__email', 'player__user__first_name', 'player__user__last_name']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Certificate, CertificateAdmin)