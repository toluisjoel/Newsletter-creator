from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from .models import Subscriber, Unsubscriber
from .tokens import account_activation_token


@receiver(post_save, sender=Subscriber)
def my_callback(sender, instance, created, **kwargs):    
    if created:
        # Delete user email from unsubscribers list, if they have once unsubscribed
        try:
            unsubscriber = Unsubscriber.objects.get(email=instance.email)
            unsubscriber.delete()
        except Unsubscriber.DoesNotExist:
            pass

        # Send Confirmation Email
        email_context = {
            'subscriber': instance,
            'action': 'added',
            'domain': '127.0.0.1:8000',  # get_current_site(request).domain
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': account_activation_token.make_token(instance),
            'protocol': 'http',  # 'https' if request.is_secure() else 'http'
        }
        html_content = render_to_string('emails/confirm_subscription.html', email_context)
        plain_text_content = strip_tags(html_content)

        send_mail(
            'Subscription Confirmation',
            plain_text_content,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            html_message=html_content,
            fail_silently=False,
        )
