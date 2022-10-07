from rest_framework import serializers

from news.models import Post
from emails.models import UserInfo


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
