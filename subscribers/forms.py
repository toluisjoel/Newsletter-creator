from django import forms

from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'email': forms.TextInput(attrs={'class': 'form-control w-50'}),
        }
