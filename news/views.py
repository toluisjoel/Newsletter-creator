from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import NewsLetter, Post
from news.forms import NewsLetterForm, PostForm

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
    template_name = 'news/previous_letters.html'
    context_object_name = 'news'

    def get_queryset(self):
        return super().get_queryset().filter(ready=True, published=True)


class NewsLetterDetail(generic.DetailView):
    model = NewsLetter
    context_object_name = 'news'
