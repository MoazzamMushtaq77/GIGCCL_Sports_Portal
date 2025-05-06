from django.shortcuts import render, redirect
from .models import Sport, Event, Notification, SportSchedule, SportGallery
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import FeedbackForm

def sports_gallery(request):
    sports_list = SportGallery.objects.all().order_by('-id')  # Optional: sort newest first
    paginator = Paginator(sports_list, 9)  # Show 9 items per page (change as needed)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sports_gallery.html', {'page_obj': page_obj})



def sports_schedules(request):
    schedules_list = SportSchedule.objects.all().order_by('-uploaded_at')
    paginator = Paginator(schedules_list, 9)  # Show 9 schedules per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sports_schedules.html', {'page_obj': page_obj})



def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})



def notification_list(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
           Q(is_general=True) | Q(recipient=request.user)
        ).order_by('-created_at')
        return render(request, 'notification_list.html', {'notifications': notifications})


def sports(request):
    sport_list = Sport.objects.all()
    paginator = Paginator(sport_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "sports.html", {"page_obj": page_obj})


def events(request):
    event_list = Event.objects.all().order_by('-date')
    paginator = Paginator(event_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "events.html", {"page_obj": page_obj})


