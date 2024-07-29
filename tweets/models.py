from django.db import models
from authentication.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.


# created : yashvi ghetiya
class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)    
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class TweetUploads(models.Model):
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE, related_name="tweet")
    file = models.FileField(upload_to="tweet-uploads")
    mime_type = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.tweet.content)
