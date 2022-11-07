from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.newsboard, name='newsboard'),
    
    # post
    path('post/', views.PostList.as_view(), name='post_list'),
    path('post/<str:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/create/', views.CreatePost.as_view(), name='create_post'),
    
    # news letter
    path('news-letter/', views.NewsLetterList.as_view(), name='letter_list'),
    path('news-letter/create/', views.CreateLetter.as_view(), name='create_letter'),
    path('news-letter/<str:pk>/', views.NewsLetterDetail.as_view(), name='letter_detail'),
    path('previous-news/', views.PreviousNewsLetterList.as_view(), name='previous_news_list'),
    path('send_newsletter/<int:pk>/', views.send_newsletter, name='send_newsletter'),
]
