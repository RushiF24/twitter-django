from django.urls import path, include
from .views import (
    TweetCommentCreateView,
    TweetCommentReplyCreateView,
    TweetCommentDisplayView,
    TweetCommentReplyDisplayView,
)
from rest_framework.routers import DefaultRouter

# created : yashvi ghetiya

app_name = "commenttweet"
router = DefaultRouter()
router.register(r"comment", TweetCommentCreateView, basename="tweet_comment")
router.register(r"getcomments", TweetCommentDisplayView, basename="tweet_comment_get")
router.register(r"reply", TweetCommentReplyCreateView, basename="tweet_comment_reply")
router.register(
    r"getreplies", TweetCommentReplyDisplayView, basename="tweet_comment_reply_get"
)
urlpatterns = [
    path("", include(router.urls)),
]
