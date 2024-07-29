from rest_framework import serializers
from .models import TweetLikes

# created : yashvi ghetiya

class DynamicLikeSerializer(serializers.ModelSerializer):
     def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class TweetLikeSerializer(DynamicLikeSerializer):
    class Meta:
        model = TweetLikes
        fields = ['tweet',]

    def create(self, validated_data):
        user = self.context.get("request").user
        tweet_like = TweetLikes.objects.create(**validated_data, user=user)
        return tweet_like

class TweetLikeGetSerializer(DynamicLikeSerializer):
    class Meta:
        model = TweetLikes
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("request").user
        tweet_like = TweetLikes.objects.create(**validated_data, user=user)
        return tweet_like