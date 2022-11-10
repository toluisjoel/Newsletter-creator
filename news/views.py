from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import NewsLetterForm, PostForm
from .models import NewsLetter, Post
from subscribers.models import Subscriber, Unsubscriber
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

@login_required
def metrics(request):
    # Subscribers metrics
    subscribers = Subscriber.objects.filter(confirmed=True)
    subs_count =  len(subscribers)
    
    unsubscribers = Unsubscriber.objects.all()
    unsubs_count = len(unsubscribers)
    
    total_user_count = subs_count + unsubs_count
    subs_percentage =  round((subs_count / total_user_count) * 100, 2)
    unsubs_percentage = round((unsubs_count / total_user_count) * 100, 2)
    
    # Email metrics
    delivered_emails = 0
    opened_emails = 0
    for subscriber in subscribers:
        delivered_emails += subscriber.delivered_emails
        opened_emails += subscriber.opened_emails
        
    total_email_count = delivered_emails + opened_emails
    delivered_percentage =  round((delivered_emails / total_email_count) * 100, 2)
    opened_percentage = round((opened_emails / total_email_count) * 100, 2)
    
    context = {
        'subscribers_count': subs_count,
        'subscribers_percentage': subs_percentage,
        'unsubscribers_percentage': unsubs_percentage,
        'unsubscribers_count': unsubs_count,
        'delivered_emails': delivered_emails,
        'delivered_percentage': delivered_percentage,
        'opened_emails': opened_emails,
        'opened_percentage': opened_percentage,
    }
    
    return render(request, 'news/metrics.html', context)


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
        return super().get_queryset().filter(published=True).order_by('-published_date')


class NewsLetterDetail(generic.DetailView):
    model = NewsLetter
    context_object_name = 'news'


@require_POST
def send_newsletter(request, pk):
    send_utility.send_news_letter(pk)
    return redirect('news:newsboard')
