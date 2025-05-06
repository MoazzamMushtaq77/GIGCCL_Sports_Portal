from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_coach = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)

