from django.contrib import admin

from .models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'created_at']

admin.site.register(UserInfo, UserInfoAdmin)
