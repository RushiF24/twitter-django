from django.db import models
from tweets.models import Tweets
from authentication.models import User
# Create your models here.


class TweetLikes(models.Model):
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE,related_name='tweet_like')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_like")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % (self.tweet.content)
    class Meta:
        unique_together = ('tweet', 'user',)