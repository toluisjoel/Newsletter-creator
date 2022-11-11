from django import forms

from .models import Subscriber, Unsubscriber

my_default_errors = {
    'unique': 'You are not a subscriber',
    'invalid': 'Enter a valid email address',
}

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'email': forms.TextInput(attrs={'class': 'form-control w-50'}),
        }

class UnsubscribeForm(forms.ModelForm):
    class Meta:
        model = Unsubscriber
        fields = ('email',)
        
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control w-50',}),
        }
        error_messages = {
            'email': my_default_errors,
        }
        
    def clean(self):
        email = self.cleaned_data.get('email')
        try:
            sub_email = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            raise forms.ValidationError('You are not a subscriber')
        return super().clean()