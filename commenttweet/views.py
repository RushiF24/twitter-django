from django.shortcuts import render
from rest_framework import viewsets,status,mixins
from rest_framework.permissions import IsAuthenticated
from .serializer import (
    TweetCommentSerializer,
    TweetReplySerializer,
    TweetCommentDisplaySerializer,
    TweetReplyDisplaySerializer,
)
from rest_framework.response import Response
from tweets.models import Tweets
from .models import TweetComments, TweetCommentReplies
from .permissions import IsOwnerOrReadOnly
from datetime import datetime

# created : yashvi ghetiya


class TweetCommentCreateView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = TweetCommentSerializer
    # queryset = TweetComments.objects.all()
    http_method_names = ['post', 'delete','patch']

    def destroy(self, request, *args, **kwargs):
        tweet_comment = self.get_object()
        if tweet_comment.deleted == True:
            return Response(
                {
                    "status": True,
                    "message": "Comment Does Exists",
                    "status_code": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            tweet = Tweets.objects.get(id=tweet_comment.tweet_id)
            if tweet.deleted == False:
                tweet_comment.deleted = True
                tweet_comment.deleted_at = datetime.utcnow()
                tweet_comment.save()
                return Response(
                    {
                        "status": True,
                        "message": "Comment SuccessFully Deleted",
                        "status_code": status.HTTP_200_OK,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "status": False,
                        "message": "Comment Not Available",
                        "status_code": status.HTTP_404_NOT_FOUND,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

    def create(self, request, *args, **kwargs):
        if request.data.get("comment_message") and request.data.get("tweet"):
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
                        data = super().create(request, *args, **kwargs)
                        print(data)
                    except Exception as e:
                        return Response(
                            {
                                "status": False,
                                "message": str(e),
                                "status_code": status.HTTP_400_BAD_REQUEST,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        return Response(
                            {
                                "status": True,
                                "message": "Commented SuccessFully on Tweet",
                                "status_code": status.HTTP_200_OK,
                                # "data":data
                            },
                            status=status.HTTP_200_OK,
                        )
        elif request.data.get("comment_message"):
            message = {"tweet": "This field is required"}
        elif request.data.get("tweet"):
            message = {"comment_message": "This field is required"}
        else:
            message = {
                "tweet": "This field is required",
                "comment_message": "This field is required",
            }
        return Response(
            {
                "status": False,
                "message": message,
                "status_code": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "status": True,
                "message": "Comment SuccessFully Updated",
                "status_code": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class TweetCommentReplyCreateView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = TweetReplySerializer
    # queryset = TweetCommentReplies.objects.all()
    http_method_names = ['post', 'delete','patch']

    def destroy(self, request, *args, **kwargs):
        comment_reply = self.get_object()
        if comment_reply.deleted == True:
            return Response(
                {
                    "status": False,
                    "message": "Reply Does Not Exists",
                    "status_code": status.HTTP_404_NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            tweet_comment = TweetComments.objects.get(id=comment_reply.tweetcomment_id)
            if tweet_comment.deleted == False:
                try:
                    tweet = Tweets.objects.get(id=tweet_comment.tweet_id)
                    if tweet.deleted == True:
                        raise Tweets.DoesNotExist()
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
                    comment_reply.deleted = True
                    comment_reply.deleted_at = datetime.utcnow()
                    comment_reply.save()
                    return Response(
                        {
                            "status": True,
                            "message": "Reply SuccessFully Deleted",
                            "status_code": status.HTTP_200_OK,
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {
                        "status": False,
                        "message": "Comment Does Not Exists",
                        "status_code": status.HTTP_404_NOT_FOUND,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

    def create(self, request, *args, **kwargs):
        if request.data.get("reply_message") and request.data.get("tweetcomment"):
            comment_id = request.data["tweetcomment"]
            try:
                comments = TweetComments.objects.get(id=comment_id)
                if comments.deleted == True:
                    raise TweetComments.DoesNotExist()
            except TweetComments.DoesNotExist:
                return Response(
                    {
                        "status": False,
                        "message": "Comment Does Not Exists",
                        "status_code": status.HTTP_404_NOT_FOUND,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                try:
                    tweet = Tweets.objects.get(id=comments.tweet_id)
                    if tweet.deleted == True:
                        raise Tweets.DoesNotExist()
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
                    try:
                        super().create(request, *args, **kwargs)
                    except Exception as e:
                        return Response(
                            {
                                "status": False,
                                "message": str(e),
                                "status_code": status.HTTP_400_BAD_REQUEST,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        return Response(
                            {
                                "status": True,
                                "message": "Reply SuccessFully on Added",
                                "status_code": status.HTTP_200_OK,
                            },
                            status=status.HTTP_200_OK,
                        )
        elif request.data.get("reply_message"):
            message = {"tweetcomment": "This field is required"}
        elif request.data.get("tweetcomment"):
            message = {"reply_message": "This field is required"}
        else:
            message = {
                "tweetcomment": "This field is required",
                "reply_message": "This field is required",
            }
        return Response(
            {
                "status": False,
                "message": message,
                "status_code": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "status": True,
                "message": "Reply SuccessFully Updated",
                "status_code": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class TweetCommentDisplayView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetCommentDisplaySerializer
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.data.get("tweet"):
            queryset = TweetComments.objects.filter(
                tweet_id=self.request.data.get("tweet"),deleted=False
            )
            return queryset
        else:
            return []


class TweetCommentReplyDisplayView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetReplyDisplaySerializer
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.data.get("comment"):
            queryset = TweetCommentReplies.objects.filter(
                tweetcomment_id=self.request.data.get("comment"),deleted=False
            )
            return queryset
        else:
            return []
