from django.urls import path,include
from .views import TweetLikeCreateView,TweetLikeDisplayView
from rest_framework.routers import DefaultRouter

#created : yashvi ghetiya
app_name='liketweet'
router = DefaultRouter()
router.register(r'like', TweetLikeCreateView,basename="tweet_like")
router.register(r'getlike',TweetLikeDisplayView,basename="tweet_like_get")
urlpatterns = [
    path('',include(router.urls)),
]