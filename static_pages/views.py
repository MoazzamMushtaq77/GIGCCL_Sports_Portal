from django.shortcuts import render, get_object_or_404
from .models import Achievements, HomePic, HODMessage
from sports_base.models import Sport, Team, MatchResult
from django.contrib.auth.decorators import login_required

def scoreboard(request):
    sports = Sport.objects.all()
    selected_sport = request.GET.get('sport')
    if selected_sport:
        matches = MatchResult.objects.filter(sport__id=selected_sport).order_by('-date')
    else:
        matches = MatchResult.objects.all().order_by('-date')

    context = {
        'sports': sports,
        'matches': matches,
        'selected_sport': selected_sport,
    }
    return render(request, 'static_pages/scoreboard.html', context)

@login_required(login_url='Sports_Users:player_login')
def teams(request):
    sports = Sport.objects.all()
    selected_sport = request.GET.get('sport')
    
    if selected_sport:
        teams = Team.objects.filter(sport__id=selected_sport).prefetch_related('players', 'achievements').select_related('coach', 'sport')
    else:
        teams = Team.objects.prefetch_related('players', 'achievements').select_related('coach', 'sport')
    
    context = {
        'teams': teams,
        'sports': sports,
        'selected_sport': selected_sport,
    }
    return render(request, 'static_pages/teams.html', context)

def home(request):
    home_pic = HomePic.objects.all()
    hod_message = HODMessage.objects.first() if HODMessage.objects.exists() else None
    return render(request, "static_pages/home.html", {
        "home_pic": home_pic,
        "hod_message": hod_message
    })

def aboutus(request):
    return render(request, "static_pages/aboutus.html")

def achievements(request):
    achievements = Achievements.objects.select_related('team').order_by('-date')
    return render(request, 'achievements.html', {'achievements': achievements})

def dev_profile(request):
    return render(request, 'static_pages/dev_profile.html')