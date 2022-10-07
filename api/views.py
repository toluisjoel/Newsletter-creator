from django.shortcuts import render

from rest_framework import mixins, viewsets
from rest_framework import permissions

from .serializers import (
    PostSerializer,
    EmailSerializer,
)
from news.models import Post
from users.models import Email


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='draft', validated=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class EmailViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [permissions.IsAdminUser]