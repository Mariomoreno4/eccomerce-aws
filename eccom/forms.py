
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ['review_text', 'rating']