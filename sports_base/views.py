from django.shortcuts import render, redirect, get_object_or_404
from .models import Sport, Event, Notification, SportSchedule, SportGallery, Team, Coach, MatchResult, Feedback
from Sports_Users.models import Player
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import FeedbackForm

def sports_gallery(request):
    sports_list = SportGallery.objects.all().order_by('-id')
    paginator = Paginator(sports_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sports_base/sports_gallery.html', {'page_obj': page_obj})

def sports_schedules(request):
    schedules_list = SportSchedule.objects.all().order_by('-uploaded_at')
    paginator = Paginator(schedules_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sports_base/sports_schedules.html', {'page_obj': page_obj})

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('sports_base:feedback')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeedbackForm()
    return render(request, 'sports_base/feedback.html', {'form': form})

def notification_list(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(is_general=True).order_by('-created_at')
        paginator = Paginator(notifications, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sports_base/notification_list.html', {'page_obj': page_obj})
    return redirect('Sports_Users:player_login')

def sports(request):
    sport_list = Sport.objects.all().order_by('name')
    paginator = Paginator(sport_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sports_base/sports.html', {'page_obj': page_obj})

def events(request):
    event_list = Event.objects.all().order_by('-date')
    paginator = Paginator(event_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sports_base/events.html', {'page_obj': page_obj})

def coach_profile(request):
    coaches = Coach.objects.all().order_by('name')
    paginator = Paginator(coaches, 9)  # Display 9 coaches per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sports_base/coach_profile.html', {'page_obj': page_obj})