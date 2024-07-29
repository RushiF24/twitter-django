from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializer import TweetLikeSerializer, TweetLikeGetSerializer
from rest_framework.response import Response
from rest_framework import status
from tweets.models import Tweets
from .models import TweetLikes
from .permissions import IsOwnerOrReadOnly

# created : yashvi ghetiya


class TweetLikeDisplayView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetLikeGetSerializer

    def get_queryset(self):
        if self.request.data.get("tweet"):
            queryset = TweetLikes.objects.filter(
                tweet_id=self.request.data.get("tweet")
            )
            return queryset
        else:
            return []

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": 'Method "POST" not allowed.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": 'Method "DELETE" not allowed.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class TweetLikeCreateView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = TweetLikeSerializer
    queryset = TweetLikes.objects.all()
    http_method_names = ["delete", "post"]

    def get_object(self): 
        return get_object_or_404(TweetLikes, tweet=self.kwargs['pk'], user=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        tweet_like = self.get_object()
        tweet = Tweets.objects.get(id=tweet_like.tweet_id)
        if tweet.deleted == False:
            try:
                tweet_like.delete()
            except:
                return Response(
                    {
                        "status": False,
                        "message": "Opps Some Error Occured Try Again!",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    {
                        "status": True,
                        "message": "Like SuccessFully Deleted",
                        "status_code": status.HTTP_200_OK,
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {
                    "status": False,
                    "message": "Tweet Not Available",
                    "status_code": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request, *args, **kwargs):
        if request.data.get("tweet"):
            tweet_id = request.data["tweet"]
            try:
                tweet = Tweets.objects.get(id=tweet_id)
            except Tweets.DoesNotExist:
                return Response(
                    {
                        "status": False,
                        "message": "Tweet Does Not Exists",
                        "status_code": status.HTTP_404_NOT_FOUND,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                if tweet.deleted == True:
                    return Response(
                        {
                            "status": False,
                            "message": "Tweet Not Accessible",
                            "status_code": status.HTTP_404_NOT_FOUND,
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
                else:
                    try:
                        response = super().create(request, *args, **kwargs)
                        # print(response)
                    except Exception as e:
                        print(e)
                        return Response(
                            {
                                "status": False,
                                "message": "Tweet Already Liked",
                                "status_code": status.HTTP_409_CONFLICT,
                            },
                            status=status.HTTP_409_CONFLICT,
                        )
                    else:
                        return Response(
                            {
                                "status": True,
                                "message": "Tweet SuccessFully Liked",
                                "status_code": status.HTTP_200_OK,
                                # "data": response.data["tweet_like_serializer"],
                            },
                            status=status.HTTP_200_OK,
                        )
        else:
            return Response(
                {
                    "status": False,
                    "message": {"tweet": "This field is required"},
                    "status_code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
