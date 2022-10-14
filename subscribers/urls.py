from django.urls import path

from . import views

app_name = 'subscribers'

urlpatterns = [
    path('', views.AddSubscriber.as_view(), name='add'),
    path('complete-subscription/', views.complete_subscription, name='complete'),
    path('confirm/<uidb64>/<token>/', views.confirm_subscriber, name='confirm'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]