from django.urls import path
from . import views
from sports_base import views as baseviews

app_name = 'sports_base'

urlpatterns = [
    path("sports/", baseviews.sports, name="sports"),
    path("events/", baseviews.events, name="events"),
    path('notifications/', baseviews.notification_list, name='notification_list'),
    path('feedback/', baseviews.feedback, name='feedback'),
    path('schedules/', baseviews.sports_schedules, name='sports_schedules'),
    path('gallery/', baseviews.sports_gallery, name='sports_gallery'),
    path('coaches/', baseviews.coach_profile, name='coach_profile'),
]