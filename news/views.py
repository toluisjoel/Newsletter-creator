from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Post, NewsLetter
from news.forms import NewsLetterForm, PostForm


def newsboard(request):
    return render(request, 'news/newsboard.html', {})


class CreateLetter(generic.CreateView):
    form_class = NewsLetterForm
    template_name = 'news/create_letter.html'
    success_url = reverse_lazy('news:letter_list')


class NewsLetterList(generic.ListView):
    model = NewsLetter
    context_object_name = 'news'


class NewsLetterDetail(generic.DetailView):
    model = NewsLetter
    context_object_name = 'news'


class PostList(generic.ListView):
    model = Post
    context_object_name = 'posts'


class PostDetail(generic.DetailView):
    model = Post
    context_object_name = 'post'


class CreatePost(generic.CreateView):
    form_class = PostForm
    template_name = 'news/create_letter.html'
    success_url = reverse_lazy('news:post_list')
