from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from news.forms import LetterForm

from .models import Post


class PostList(generic.ListView):
    model = Post
    context_object_name = 'posts'


class create_letter(generic.CreateView):
    form_class = LetterForm
    template_name = 'news/create_letter.html'
    success_url = reverse_lazy('news:post_list')
