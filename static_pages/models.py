# static_pages/models.py
# static_pages/models.py
from django.db import models
from django.db import models

class Sports(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Match(models.Model):
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.team1} vs {self.team2} ({self.sport.name})"


class Coach(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    is_captain = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    players = models.ManyToManyField(Player)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return self.title

class Achievements(models.Model):
    team = models.ForeignKey(Team, related_name='achievement_set', on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.team.name} achievements"