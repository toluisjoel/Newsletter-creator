from attr import fields
from django import forms

from .models import NewsLetter, Post

class NewsLetterForm(forms.ModelForm):
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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'source', 'image')