from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from .forms import SubscribeForm
from .models import Subscriber, Unsubscriber
from .tokens import account_activation_token


class AddSubscriber(generic.CreateView):
    form_class = SubscribeForm
    template_name = 'index.html'
    success_url = reverse_lazy('subscribers:complete')


def complete_subscription(request):
    return render(request, 'complete_subscription.html', {})


def confirm_subscriber(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        subscriber = Subscriber.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Subscriber.DoesNotExist):
        subscriber = None

    if subscriber is not None and account_activation_token.check_token(subscriber, token):
        subscriber.confirmed = True
        subscriber.save()
    else:
        return HttpResponse('You were wrong. psych!')

    return render(request, 'index.html', {'action': 'confirmed'})


def unsubscribe(request):
    subscriber = Subscriber.objects.get(email=request.GET['email'])
    if subscriber.otp_num == request.GET['otp_num']:
        Unsubscriber.objects.create(
            first_name=subscriber.first_name,
            last_name=subscriber.last_name,
            email=request.GET['email']
        )
        subscriber.delete()
        return render(request, 'index.html', {'email': subscriber.email, 'action': 'unsubscribed'})

    return render(request, 'index.html', {'email': subscriber.email, 'action': 'denied'})
