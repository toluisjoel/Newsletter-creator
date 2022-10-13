from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import SubscribeForm
from .models import Subscriber, Unsubscriber
from .tokens import account_activation_token


def add_subscriber(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            validate_email(subscriber.email)
            form.save()

            # Delete user email from unsubscribers list, if they have once unsubscribed
            try:
                unsubscriber = Unsubscriber.objects.get(email=subscriber.email)
                unsubscriber.delete()
            except Unsubscriber.DoesNotExist:
                pass

            # Send Confirmation Email
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

    else:
        form = SubscribeForm()
    return render(request, 'index.html', {'form': form})


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
