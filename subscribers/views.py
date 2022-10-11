import random

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .forms import SubscribeForm
from .models import Subscriber, Unsubscriber
from .tokens import account_activation_token


def otp_number():
    return "%0.12d" % random.randint(0, 999999999999)


@csrf_exempt
def add_subscriber(request):
    if request.method == 'POST':
        subscriber = Subscriber(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            otp_num=otp_number()
        )
        subscriber.save()

        # Delete user email from unsubscribers list, if they have once unsubscribed
        try:
            unsubscriber = Unsubscriber.objects.get(
                email=request.POST['email'])
            unsubscriber.delete()
        except Unsubscriber.DoesNotExist:
            pass
        
        email_context = {
            'subscriber': subscriber,
            'action': 'added',
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(subscriber.pk)),
            'token': account_activation_token.make_token(subscriber),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        html_content = render_to_string('confirm_subscription.html', email_context)
        plain_text_content = strip_tags(html_content)

        send_mail(
            'Subscription Confirmation',
            plain_text_content,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        context = {
            'subscriber': subscriber,
            'action': 'subscribed',
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html', {'form': SubscribeForm})


def confirm_subscriber(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        subscriber = Subscriber.objects.get(pk=uid)
    except:
        subscriber = None

    if (subscriber is not None) and (account_activation_token.check_token(subscriber, token)):
        subscriber.confirmed = True
        subscriber.save()

    else:
        return HttpResponse('There was an error confirming your email address')
    
    return redirect('subscribers:add')


def unsubscribe(request):
    subscriber = Subscriber.objects.get(email=request.GET['email'])
    if subscriber.otp_num == request.GET['otp_num']:
        Unsubscriber.objects.create(first_name=subscriber.first_name,
                                    last_name=subscriber.last_name,
                                    email=request.GET['email']
                                    )
        subscriber.delete()  
        return render(request, 'index.html', {'email': subscriber.email, 'action': 'unsubscribed'})

    return render(request, 'index.html', {'email': subscriber.email, 'action': 'denied'})
