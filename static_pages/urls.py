from django.urls import path
from . import views

app_name = 'static_pages'

urlpatterns = [
    path("", views.home, name="home"),
    path("teams/", views.teams, name='teams'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path("about/", views.aboutus, name="aboutus"),
    path('developer-profile/', views.dev_profile, name='dev_profile'),
]