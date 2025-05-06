from django.contrib import admin

# Register your models here.
from Sports_Users.models import CustomUser
admin.site.register(CustomUser)