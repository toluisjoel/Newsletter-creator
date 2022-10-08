from django.contrib import admin

from .models import Subscriber, Unsubscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'confirmed']
    list_filter = ['confirmed', 'created_at']


class UnubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'created_at']
    list_filter = ['created_at']


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Unsubscriber, UnubscriberAdmin)
