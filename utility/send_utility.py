from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from news.models import NewsLetter
from subscribers.models import Subscriber


def send_confirmation_mail(recepient_email, plain_text, html_content):
    send_mail(
        'Subscription confirmation',
        plain_text,
        settings.DEFAULT_FROM_EMAIL,
        [recepient_email],
        html_message=html_content,
        fail_silently=False,
    )
    subscriber = Subscriber.objects.get(email=recepient_email)
    subscriber.delivered_emails += 1
    subscriber.save()


def send_letter(pk):
    news = NewsLetter.objects.get(id=pk)
    subscribers = Subscriber.objects.filter(confirmed=True)

    email_context = {
        'news': news,
        'posts': news.posts,
    }
    html_content = render_to_string('emails/news_letter.html', email_context)
    plain_text_content = strip_tags(html_content)

    send_mail(
        news.title,
        plain_text_content,
        settings.DEFAULT_FROM_EMAIL,
        [subscriber.email for subscriber in subscribers],
        html_message=html_content,
        fail_silently=False,
    )
    for subscriber in subscribers:
        subscriber.delivered_emails += 1
        subscriber.save()