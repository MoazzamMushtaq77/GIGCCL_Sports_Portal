from django.contrib import admin
from .models import Achievements, HomePic, HODMessage


@admin.register(Achievements)
class AchievementsAdmin(admin.ModelAdmin):
    list_display = ('description', 'team')
    list_filter = ('team',)
    search_fields = ('description', 'team__name')

@admin.register(HomePic)
class HomePicAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    search_fields = ('id',)
    list_filter = ('created_at',)

@admin.register(HODMessage)
class HODMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at')
    search_fields = ('name', 'message')
    list_filter = ('updated_at',)