from django.contrib import admin

from .models import Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'created_at']

admin.site.register(Email, EmailAdmin)
