from django.db import models


class Subscriber(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(blank=True, max_length=25)
    email = models.EmailField(unique=True)

    otp_num = models.CharField(max_length=50)
    confirmed = models.BooleanField(default=False)  # True if subscriber confirms email

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Unsubscriber(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(blank=True, max_length=25)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email