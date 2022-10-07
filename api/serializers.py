from rest_framework import serializers

from news.models import Post
from users.models import Email


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
        ]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
