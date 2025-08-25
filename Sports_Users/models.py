from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


def restrict_file_to_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('File must be a PDF.')


# Custom manager to avoid username requirement
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Auto-generate username from email if not provided
        if not extra_fields.get('username'):
            extra_fields['username'] = email.split('@')[0]
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    is_coach = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cnic = models.CharField(max_length=15, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # Kept for backward compatibility
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Only email and password required

    objects = CustomUserManager()  # Use custom manager

    def save(self, *args, **kwargs):
        if not self.username:
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        self.is_approved = (self.status == 'approved')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def plain_password(self):
        return self.password


class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='player')
    father_name = models.CharField(max_length=100)
    father_cnic = models.CharField(max_length=15)
    dob = models.DateField()
    whatsapp_number = models.CharField(max_length=15, blank=True)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    sport = models.ForeignKey('sports_base.Sport', on_delete=models.SET_NULL, null=True)
    height = models.FloatField()
    weight = models.FloatField()
    college_roll_no = models.CharField(max_length=50)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    DISABILITY_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    disability = models.CharField(max_length=3, choices=DISABILITY_CHOICES, blank=True)
    disability_detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Player: {self.user.first_name} {self.user.last_name}"


class Certificate(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=255)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    # , validators=[restrict_file_to_pdf]
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.player.user.first_name} {self.player.user.last_name}"
