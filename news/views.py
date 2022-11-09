from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from .models import NewsLetter, Post
from news.forms import NewsLetterForm, PostForm
from utility import send_utility


# Post
class CreatePost(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'news/create_post.html'
    success_url = reverse_lazy('news:post_list')


class PostList(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'


class PostDetail(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'


# News Letter
@login_required
def newsboard(request):
    return render(request, 'news/newsboard.html', {})


class CreateLetter(LoginRequiredMixin, generic.CreateView):
    form_class = NewsLetterForm
    template_name = 'news/create_letter.html'
    success_url = reverse_lazy('news:letter_list')


class NewsLetterList(LoginRequiredMixin, generic.ListView):
    model = NewsLetter
    context_object_name = 'news'


class PreviousNewsLetterList(generic.ListView):
    model = NewsLetter
    template_name = 'news/previous_newsletters.html'
    context_object_name = 'previous_newsletters'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class NewsLetterDetail(generic.DetailView):
    model = NewsLetter
    context_object_name = 'news'


@require_POST
def send_newsletter(request, pk):
    send_utility.send_news_letter(pk)
    return redirect('news:newsboard')
