from rest_framework import serializers
from .models import Follow
from django.contrib.auth import get_user_model

from authentication.serializers import UserSerializer

User = get_user_model()

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']


class FollowingsSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']
class FollowersSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']