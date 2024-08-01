from rest_framework import serializers
from .models import TweetComments,TweetCommentReplies
from authentication.serializers import UserSerializer

# created : yashvi ghetiya

class DynamicSerializer(serializers.ModelSerializer):
     def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class TweetCommentSerializer(DynamicSerializer):

    user = UserSerializer(read_only=True)
    class Meta:
        model = TweetComments
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("request").user
        tweet_comment = TweetComments.objects.create(**validated_data, user=user)
        return tweet_comment

class TweetCommentDisplaySerializer(DynamicSerializer):

    user = UserSerializer()
    class Meta:
        model = TweetComments
        fields = "__all__"

class TweetReplySerializer(DynamicSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = TweetCommentReplies
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("request").user
        tweet_comment = TweetCommentReplies.objects.create(**validated_data, user=user)
        return tweet_comment

class TweetReplyDisplaySerializer(DynamicSerializer):
    user = UserSerializer()
    class Meta:
        model = TweetCommentReplies
        fields = "__all__"