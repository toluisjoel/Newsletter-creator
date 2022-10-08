import random

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

from .forms import SubscribeForm
from .models import Subscriber, Unsubscriber


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
        except:
            pass

        html_content = 'Hey {}! thank you for signing up for our email NEWSletter! <a href="{}?email={}&otp_num={}"></a>'.format(
            subscriber.first_name, request.build_absolute_uri(reverse('subscribers:confirm')), subscriber.email, subscriber.otp_num)

        # message = Mail(from_email=settings.FROM_EMAIL,
        #                to_emails=subscriber.email,
        #                subject='Newsletter Confirmation',
        #                html_content='Thank you for signing up for my email newsletter! \
        #                 Please complete the process by \
        #                 <a href="{}?email={}&conf_num={}"> clicking here to \
        #                 confirm your registration</a>.'.format(
        #                    request.build_absolute_uri(reverse('subscribers:confirm')),
        #                    subscriber.email,
        #                    subscriber.otp_num)
        #                )

        # send_grid = SendGridAPIClient(settings.SENDGRID_API_KEY)
        # send_grid.send(message)

        send_mail(
            'Django mail',
            html_content,
            'your_account@gmail.com',
            [subscriber.email],
            fail_silently=False
        )

        context = {
            'email': subscriber.email,
            'action': 'added',
            'form': SubscribeForm(),
        }

        return render(request, 'index.html', context)

    return render(request, 'index.html', {'form': SubscribeForm})


def confirm_subscriber(request):
    subscriber = Subscriber.objects.get(email=request.GET['email'])

    if subscriber.otp_num == request.GET['otp_num']:
        subscriber.confirmed = True
        subscriber.save()

        return render(request, 'index.html', {'email': subscriber.email, 'action': 'confirmed'})

    return render(request, 'index.html', {'email': subscriber.email, 'action': 'denied'})


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
