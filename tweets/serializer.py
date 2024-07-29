from rest_framework import serializers
from .models import Tweets, TweetUploads
from django.core.validators import FileExtensionValidator
from authentication.serializers import UserSerializer
from liketweet.serializer import TweetLikeGetSerializer
from commenttweet.serializer import TweetCommentDisplaySerializer

# created : yashvi ghetiya


class DynamicSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TweetUploadsSerializer(DynamicSerializer):
    class Meta:
        model = TweetUploads
        fields = "__all__"


class TweetDisplaySerializer(DynamicSerializer):
    tweet = TweetUploadsSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    tweet_like = TweetLikeGetSerializer(many=True, read_only=True)
    tweet_comment = TweetCommentDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Tweets
        fields = "__all__"


class TweetSerializer(serializers.ModelSerializer):
    images = TweetUploadsSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False,
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["png", "jpeg", "jpg", "mp4", "webp", "gif"]
                )
            ],
        ),
        write_only=True,
        required=False,
    )

    tweet_serializer = serializers.SerializerMethodField()

    class Meta:
        model = Tweets
        fields = ["content", "images", "uploaded_images", "tweet_serializer"]

    def get_tweet_serializer(self, tweet):
        return TweetDisplaySerializer(tweet).data

    def create(self, validated_data):
        user = self.context.get("request").user
        content = None
        if "content" in validated_data.keys():
            content = validated_data["content"]

        product = Tweets.objects.create(content=content, user=user)

        if "uploaded_images" in validated_data.keys():
            uploaded_images = validated_data.pop("uploaded_images")
            print(uploaded_images)
            for image in uploaded_images:
                TweetUploads.objects.create(
                    tweet=product, file=image, mime_type=image.content_type
                )

        return product
