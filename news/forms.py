from attr import fields
from django import forms

from .models import NewsLetter, Post

class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ('title', 'posts', 'ready')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'posts': forms.CheckboxSelectMultiple(attrs={'class': 'form-control w-50'}),
        }
    posts = forms.ModelMultipleChoiceField(
        queryset=Post.objects.filter(validated=True, status='draft'),
        widget=forms.CheckboxSelectMultiple
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'source', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'content': forms.Textarea(attrs={'class': 'form-control w-50'}),
            'source': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'image': forms.TextInput(attrs={'class': 'form-control w-50', 'placeholder': 'Image url (optional)'}),
        }