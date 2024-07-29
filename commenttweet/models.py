from django.db import models
from authentication.models import User
from tweets.models import Tweets

# created : yashvi ghetiya


class TweetComments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comment"
    )
    tweet = models.ForeignKey(
        Tweets, on_delete=models.CASCADE, related_name="tweet_comment"
    )
    comment_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.comment_message

class TweetCommentReplies(models.Model):
    tweetcomment=models.ForeignKey(
        TweetComments, on_delete=models.CASCADE, related_name="tweet_comment_reply"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reply"
    )
    reply_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.reply_message
