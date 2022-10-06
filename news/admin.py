from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'created_at', 'status', 'validated']
    list_filter = ['validated', 'status', 'created_at']
    list_per_page = 10

admin.site.register(Post, PostAdmin)