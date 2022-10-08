from django.db import models


class Subscriber(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(blank=True, max_length=25)
    email = models.EmailField(unique=True)

    otp_number = models.CharField(max_length=6)
    active = models.BooleanField(default=False)  # True if subscriber confirms email

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
