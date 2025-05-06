from django.shortcuts import render
from .models import News, Team
from .models import Sports, Match

def scoreboard(request):
    sports = Sports.objects.all()
    selected_sport = request.GET.get('sport')
    if selected_sport:
        matches = Match.objects.filter(sport__id=selected_sport).order_by('-date')
    else:
        matches = Match.objects.all().order_by('-date')

    context = {
        'sports': sports,
        'matches': matches,
        'selected_sport': selected_sport,
    }
    return render(request, 'scoreboard.html', context)



def teams(request):
    teams = Team.objects.prefetch_related('players', 'achievement_set').select_related('coach')
    return render(request, 'teams.html', {'teams': teams})



# View for Homepage
def home(request):
    latest_news = News.objects.order_by('-date')[:4]  # Get latest 6 news items
    return render(request, "base.html", {"latest_news": latest_news})

# View for About Us page
def aboutus(request):
    return render(request, "aboutus.html")