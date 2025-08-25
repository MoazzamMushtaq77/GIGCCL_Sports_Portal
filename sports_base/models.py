from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class SportGallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sports_gallery/')

    def __str__(self):
        return self.title

class SportSchedule(models.Model):
    title = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    image = models.ImageField(upload_to='schedules/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.season})"

class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    email = models.EmailField(max_length=254)
    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.TextField()
    suggestions = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rating: {self.rating} - {self.description[:30]}...'

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='sports_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Coach(models.Model):
    DESIGNATION_CHOICES = [
        ('head_coach', 'Head Coach'),
        ('coach', 'Coach'),
        ('assistant_coach', 'Assistant Coach'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES, default='coach')
    experience_years = models.PositiveIntegerField()
    sports = models.ManyToManyField(Sport, related_name='coaches')  # Changed to ManyToManyField
    photo = models.ImageField(upload_to='coaches/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {', '.join(sport.name for sport in self.sports.all())}"

    def save(self, *args, **kwargs):
        if self.user and not self.user.is_coach:
            self.user.is_coach = True
            self.user.save()
        super().save(*args, **kwargs)

class Team(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='teams')
    players = models.ManyToManyField('Sports_Users.Player', related_name='teams')
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, related_name='teams')
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.sport.name}"

class MatchResult(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='matches')
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches', null=True, blank=True)
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches', null=True, blank=True)
    player1 = models.ForeignKey('Sports_Users.Player', on_delete=models.CASCADE, related_name='matches_as_player1', null=True, blank=True)
    player2 = models.ForeignKey('Sports_Users.Player', on_delete=models.CASCADE, related_name='matches_as_player2', null=True, blank=True)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='scheduled')
    result = models.CharField(max_length=20, choices=[
        ('team1_win', 'Team 1 Won'),
        ('team2_win', 'Team 2 Won'),
        ('player1_win', 'Player 1 Won'),
        ('player2_win', 'Player 2 Won'),
        ('draw', 'Match Draw'),
        ('pending', 'Result Pending')
    ], default='pending')

    def save(self, *args, **kwargs):
        if self.status == 'completed':
            if self.score1 > self.score2:
                if self.team1 and self.team2:
                    self.result = 'team1_win'
                else:
                    self.result = 'player1_win'
            elif self.score2 > self.score1:
                if self.team1 and self.team2:
                    self.result = 'team2_win'
                else:
                    self.result = 'player2_win'
            else:
                self.result = 'draw'
        super().save(*args, **kwargs)

    def get_result_display_text(self):
        if self.status != 'completed':
            return 'Match not completed'
        if self.result == 'team1_win':
            return f'{self.team1.name} Won'
        elif self.result == 'team2_win':
            return f'{self.team2.name} Won'
        elif self.result == 'player1_win':
            return f'{self.player1.user.first_name} {self.player1.user.last_name} Won'
        elif self.result == 'player2_win':
            return f'{self.player2.user.first_name} {self.player2.user.last_name} Won'
        else:
            return 'Match Draw'

    def get_participants_display(self):
        if self.team1 and self.team2:
            return f"{self.team1.name} vs {self.team2.name}"
        elif self.player1 and self.player2:
            return f"{self.player1.user.first_name} {self.player1.user.last_name} vs {self.player2.user.first_name} {self.player2.user.last_name}"
        return "Invalid Match"

    def __str__(self):
        return f"{self.get_participants_display()} ({self.sport.name})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_general = models.BooleanField(default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {'General' if self.is_general else self.recipient.username}"