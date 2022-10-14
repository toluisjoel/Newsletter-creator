from pyexpat import model
from django import forms

from .models import NewsLetter, Post

class LetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ('title', 'posts', 'ready')
        widgets = {
            'posts': forms.CheckboxSelectMultiple
        }
    posts = forms.ModelMultipleChoiceField(
        queryset=Post.objects.filter(validated=True, status='draft'),
        widget=forms.CheckboxSelectMultiple
    )