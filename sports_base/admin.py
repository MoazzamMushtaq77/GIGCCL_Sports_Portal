from django.contrib import admin
from sports_base.models import Event, Sport, Notification, Feedback, SportSchedule, SportGallery


admin.site.register(SportGallery)


@admin.register(SportSchedule)
class SportScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'season', 'uploaded_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('rating', 'submitted_at')
    search_fields = ('description', 'suggestions')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_general', 'recipient', 'created_at')
    list_filter = ('is_general', 'created_at')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Event)
admin.site.register(Sport)
