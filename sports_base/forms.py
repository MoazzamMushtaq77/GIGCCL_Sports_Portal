from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['email', 'rating', 'description', 'suggestions']
        widgets = {
            'rating': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'suggestions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not 1 <= rating <= 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating