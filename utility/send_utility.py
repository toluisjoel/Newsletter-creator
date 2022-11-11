from datetime import date

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from news.models import NewsLetter, Post
from subscribers.models import Subscriber, Unsubscriber


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


def send_news_letter(pk):
    news = NewsLetter.objects.get(id=pk)
    posts = news.posts.all()
    subscribers = Subscriber.objects.filter(confirmed=True)

    email_context = {
        'news': news,
        'posts': posts,
    }
    html_content = render_to_string('emails/news_letter.html', email_context)
    plain_text_content = strip_tags(html_content)

    try:
        send_mail(
            news.title,
            plain_text_content,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email for subscriber in subscribers],
            html_message=html_content,
            fail_silently=False,
        )
        news.published = True
        news.published_date = timezone.now()
        news.save()

        for subscriber in subscribers:
            subscriber = subscriber
            subscriber.delivered_emails += 1
            subscriber.save()

        for post in posts:
            sent_post = post
            sent_post.status = 'published'
            sent_post.save()

    except:
        pass


def send_re_engagement_mail():
    unsubscribers = Unsubscriber.objects.filter(created_at='now')
    
    html_content = render_to_string('emails/re_engagement.html', {})
    plain_text_content = strip_tags(html_content)
    
    send_mail(
        'Re-engagement Mail',
        plain_text_content,
        settings.DEFAULT_FROM_EMAIL,
        [unsubscriber.email for unsubscriber in unsubscribers],
        html_message=html_content,
        fail_silently=False,
    )
