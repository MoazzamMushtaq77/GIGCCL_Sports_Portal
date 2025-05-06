from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class SportGallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='sports_gallery/')

    def __str__(self):
        return self.title


class SportSchedule(models.Model):
    title = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    image = models.ImageField(upload_to='schedules/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.season})"


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.TextField()
    suggestions = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rating: {self.rating} - {self.description[:30]}...'



class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image=models.ImageField(upload_to="sports_images/",null=True,blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    date=models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    description=models.TextField()
    def __str__(self):
        return f"{self.title}"
    

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_general = models.BooleanField(default=False)  # True = general, False = user-specific
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # optional for general

    def __str__(self):
        return f"{self.title} - {'General' if self.is_general else self.recipient.username}"

