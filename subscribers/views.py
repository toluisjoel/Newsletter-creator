from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from PIL import Image

from .forms import SubscribeForm, UnsubscribeForm
from .models import Subscriber
from .tokens import account_activation_token
from news.models import NewsLetter
from utility.send_utility import send_confirmation_mail


def add_subscriber(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            form.save()
            
            # Send Confirmation Email
            email_context = {
                'subscriber': subscriber,
                'action': 'added',
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(subscriber.pk)),
                'token': account_activation_token.make_token(subscriber),
                'protocol': 'https' if request.is_secure() else 'http',
            }
            html_content = render_to_string('emails/confirm_subscription.html', email_context)
            plain_text_content = strip_tags(html_content)
            send_confirmation_mail(subscriber.email, plain_text_content, html_content)
            
            context = {
                'subscriber': subscriber,
            }
            return render(request, 'subscribers/subscription_complete.html', context)
    else:
        form = SubscribeForm()
    previous_newsletters = NewsLetter.objects.filter(published=True).order_by('-published_date')
    
    context = {
        'form': form,
        'previous_newsletters': previous_newsletters,
    }
    return render(request, 'subscribers/add_subscriber.html', context)


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
        return HttpResponse('Something went wrong, please try again')

    return render(request, 'subscribers/subscription_complete.html', {'subscriber': subscriber})


def unsubscribe(request):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            unsubcriber = form.save(commit=False)
            subscriber = Subscriber.objects.get(email=unsubcriber.email)
            unsubcriber.first_name = subscriber.first_name
            unsubcriber.last_name = subscriber.last_name
            unsubcriber.delivered_emails = subscriber.delivered_emails
            unsubcriber.opened_emails = subscriber.opened_emails
            unsubcriber.save()
            subscriber.delete()
            
            context = {'unsubcriber': unsubcriber}
            return render(request, 'subscribers/unsubscribe_complete.html', context)
    else:
        form = UnsubscribeForm()

    context = {'form': form}

    return render(request, 'subscribers/unsubscribe.html', context)


# For tracking if user opens email
def image_load(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        subscriber = Subscriber.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Subscriber.DoesNotExist):
        subscriber = None

    if subscriber is not None and account_activation_token.check_token(subscriber, token):
        subscriber.opened_emails += 1
        subscriber.save()
        red = Image.new('RGB', (1, 1))
        response = HttpResponse(content_type='image/png')
        red.save(response, 'PNG')
        return response
    else:
        return HttpResponse('Something went wrong')
