from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'description', 'suggestions']
        widgets = {
            'rating': forms.HiddenInput(),  # We'll handle this in JS
            'description': forms.Textarea(attrs={'rows': 4}),
            'suggestions': forms.Textarea(attrs={'rows': 4}),
        }
