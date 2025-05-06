from django.contrib import admin
from django.urls import path
from static_pages import views
from django.conf import settings
from django.conf.urls.static import static
from sports_base import views as baseviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("teams/", views.teams, name='teams'),  # Fixed URL for teams page
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path("about/", views.aboutus, name="aboutus"),
    path("sports/", baseviews.sports, name="sports"),
    path("events/", baseviews.events, name="events"), 
    path('notifications/', baseviews.notification_list, name='notification_list'),
    path('feedback/', baseviews.feedback, name='feedback'),
    path('schedules/', baseviews.sports_schedules, name='sports_schedules'),
    path('gallery/', baseviews.sports_gallery, name='sports_gallery'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
