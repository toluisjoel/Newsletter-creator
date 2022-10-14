from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.newsboard, name='newsboard'),
    path('post/', views.PostList.as_view(), name='post_list'),
    path('post/<str:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('create/post/', views.CreatePost.as_view(), name='create_post'),
    path('letter/', views.NewsLetterList.as_view(), name='letter_list'),
    path('create/letter/', views.CreateLetter.as_view(), name='create_letter'),
    path('letter/<str:pk>/', views.NewsLetterDetail.as_view(), name='letter_detail'),
]