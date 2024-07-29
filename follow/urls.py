from django.urls import path
from .views import FollowUserView, UnFollowUserView, ListFollowerUserView, ListFollowingUserView

urlpatterns = [
    path('follow', FollowUserView.as_view(), name="follow-user"),
    path('unfollow/<str:username>', UnFollowUserView.as_view(), name="unfollow-user"),
    path('followers', ListFollowerUserView.as_view(), name="list-followers"),
    path('followers/<str:username>', ListFollowerUserView.as_view(), name="list-user-followers"),
    path('followings', ListFollowingUserView.as_view(), name="list-followings"),
    path('followings/<str:username>', ListFollowingUserView.as_view(), name="list-followings"),
]