from django.shortcuts import render

from rest_framework import mixins, viewsets
from rest_framework import permissions

from .serializers import (
    PostSerializer,
    UserInfoSerializer,
)
from news.models import Post
from emails.models import UserInfo


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='draft', validated=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class UserInfoViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer