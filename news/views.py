from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Post
from .serializers import PostSerializer


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='draft', validated=True)
    serializer_class = PostSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
