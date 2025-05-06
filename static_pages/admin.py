from django.contrib import admin
from .models import News, Team, Player, Coach, Achievements
from .models import Sports, Match

admin.site.register(Sports)
admin.site.register(Match)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'number', 'is_captain')
    list_filter = ('position', 'is_captain')
    search_fields = ('name',)

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'experience_years')
    search_fields = ('name', 'designation')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'coach')
    filter_horizontal = ('players',)
    search_fields = ('name', 'sport')

admin.site.register(News)
admin.site.register(Achievements)