from django.shortcuts import render
from django.views import generic

from .models import Post


class PostList(generic.ListView):
    model = Post
    context_object_name = 'posts'
