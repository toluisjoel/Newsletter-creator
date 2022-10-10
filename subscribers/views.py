import random

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils.html import strip_tags
from django.template.loader import render_to_string

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
        except Unsubscriber.DoesNotExist:
            pass
        
        confirmation_url = request.build_absolute_uri(reverse('subscribers:confirm')) + f'?email={subscriber.email}'
        email_context = {
            'subscriber': subscriber,
            'action': 'added',
            'confirmation_url': confirmation_url,
        }
        html_content = render_to_string('confirm_subscription.html', email_context)
        plain_text_content = strip_tags(html_content)

        # message = Mail(
        #     from_email=settings.FROM_EMAIL,
        #     to_emails=subscriber.email,
        #     subject='Subscription Confirmation',
        #     plain_text_content=plain_text_content,
        #     html_content=html_content,
        # )

        # send_grid = SendGridAPIClient(settings.SENDGRID_API_KEY)
        # send_grid.send(message)

        send_mail(
            'Subscription Confirmation',
            plain_text_content,
            settings.FROM_EMAIL,
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
