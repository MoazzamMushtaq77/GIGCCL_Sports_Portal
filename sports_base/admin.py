from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Sport, Team, MatchResult, Event, Notification, SportSchedule, SportGallery, Feedback, Coach
from Sports_Users.models import CustomUser, Player

class NotificationAdminForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = CustomUser.objects.filter(is_player=True)

class TeamAdminForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'sport': forms.Select,  # Use dropdown for sport
            'coach': forms.Select,  # Use dropdown for coach
            'players': FilteredSelectMultiple("Players", is_stacked=False),  # Ensure multi-select widget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter players based on selected sport
        if 'sport' in self.data:
            try:
                sport_id = int(self.data.get('sport'))
                self.fields['players'].queryset = Player.objects.filter(sport_id=sport_id, user__is_player=True)
            except (ValueError, TypeError):
                # Fallback to all players if sport is not selected or invalid
                self.fields['players'].queryset = Player.objects.filter(user__is_player=True)
        elif self.instance.pk and self.instance.sport:
            # For existing team, filter players by the team's sport
            self.fields['players'].queryset = Player.objects.filter(sport=self.instance.sport, user__is_player=True)
        else:
            # Default to all players if no sport is selected
            self.fields['players'].queryset = Player.objects.filter(user__is_player=True)
        # Filter coaches to only those associated with the selected sport
        if 'sport' in self.data:
            try:
                sport_id = int(self.data.get('sport'))
                self.fields['coach'].queryset = Coach.objects.filter(sports__id=sport_id)
            except (ValueError, TypeError):
                self.fields['coach'].queryset = Coach.objects.all()
        elif self.instance.pk and self.instance.sport:
            self.fields['coach'].queryset = Coach.objects.filter(sports__id=self.instance.sport.id)
        else:
            self.fields['coach'].queryset = Coach.objects.all()

class CoachAdminForm(forms.ModelForm):
    sports = forms.ModelMultipleChoiceField(
        queryset=Sport.objects.all(),
        widget=FilteredSelectMultiple("Sports", is_stacked=False),
        required=True
    )
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_coach=True),
        widget=forms.Select,  # Ensures dropdown menu
        required=True
    )

    class Meta:
        model = Coach
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(is_coach=True)

class MatchResultAdminForm(forms.ModelForm):
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select,
        required=True
    )
    team1 = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select,
        required=False
    )
    team2 = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select,
        required=False
    )
    player1 = forms.ModelChoiceField(
        queryset=Player.objects.filter(user__is_player=True),
        widget=forms.Select,
        required=False
    )
    player2 = forms.ModelChoiceField(
        queryset=Player.objects.filter(user__is_player=True),
        widget=forms.Select,
        required=False
    )

    class Meta:
        model = MatchResult
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure team1 and team2 only show teams for the selected sport
        if 'sport' in self.data:
            try:
                sport_id = int(self.data.get('sport'))
                self.fields['team1'].queryset = Team.objects.filter(sport_id=sport_id)
                self.fields['team2'].queryset = Team.objects.filter(sport_id=sport_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.sport:
            self.fields['team1'].queryset = Team.objects.filter(sport=self.instance.sport)
            self.fields['team2'].queryset = Team.objects.filter(sport=self.instance.sport)

        # Ensure player1 and player2 only show players associated with selected teams
        if 'team1' in self.data and 'team2' in self.data:
            try:
                team1_id = int(self.data.get('team1'))
                team2_id = int(self.data.get('team2'))
                if team1_id:
                    self.fields['player1'].queryset = Player.objects.filter(teams__id=team1_id, user__is_player=True)
                if team2_id:
                    self.fields['player2'].queryset = Player.objects.filter(teams__id=team2_id, user__is_player=True)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and (self.instance.team1 or self.instance.team2):
            if self.instance.team1:
                self.fields['player1'].queryset = Player.objects.filter(teams=self.instance.team1, user__is_player=True)
            if self.instance.team2:
                self.fields['player2'].queryset = Player.objects.filter(teams=self.instance.team2, user__is_player=True)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm
    list_display = ['name', 'sport', 'coach']
    list_filter = ['sport']
    search_fields = ['name']
    filter_horizontal = ['players']  # Keep players as filter_horizontal for multi-select

@admin.register(MatchResult)
class MatchAdmin(admin.ModelAdmin):
    form = MatchResultAdminForm
    list_display = ['sport', 'get_participants', 'date', 'status']
    list_filter = ['sport', 'status', 'date']
    search_fields = ['sport__name', 'team1__name', 'team2__name', 'player1__user__email', 'player2__user__email']
    list_per_page = 25

    def get_participants(self, obj):
        return obj.get_participants_display()
    get_participants.short_description = 'Participants'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location']
    list_filter = ['date']
    search_fields = ['title', 'location']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    list_display = ['title', 'created_at', 'is_general', 'recipient']
    list_filter = ['is_general', 'created_at']
    search_fields = ['title', 'message', 'recipient__email']

@admin.register(SportSchedule)
class SportScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'season', 'uploaded_at']
    list_filter = ['season', 'uploaded_at']
    search_fields = ['title']

@admin.register(SportGallery)
class SportGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['rating', 'description', 'submitted_at']
    list_filter = ['rating', 'submitted_at']
    search_fields = ['description', 'suggestions']

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    form = CoachAdminForm
    list_display = ['name', 'designation', 'experience_years', 'get_sports', 'user']
    list_filter = ['designation', 'sports']
    search_fields = ['name', 'user__email', 'user__first_name', 'user__last_name']
    filter_horizontal = ['sports']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user').prefetch_related('sports')

    def get_sports(self, obj):
        return ", ".join(sport.name for sport in obj.sports.all())
    get_sports.short_description = 'Sports'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = CustomUser.objects.filter(is_coach=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)