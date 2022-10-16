from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from .models import Subscriber, Unsubscriber
from .tokens import account_activation_token


@receiver(pre_save, sender=Subscriber)
def my_callback(sender, instance, **kwargs):
    try:
        unsubscriber = Unsubscriber.objects.get(email=instance.email)
        unsubscriber.delete()
    except Unsubscriber.DoesNotExist:
        pass

