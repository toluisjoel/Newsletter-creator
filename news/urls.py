from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('post-list/', views.PostList.as_view(), name='post_list'),
]