from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .serializer import TweetSerializer, TweetDisplaySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Tweets
from .permissions import IsOwnerOrReadOnly
from django.db.models import Count
from rest_framework.views import APIView

# created : yashvi ghetiya


class TweetCreateView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    parser_class = [MultiPartParser, FormParser, FileUploadParser]
    serializer_class = TweetSerializer
    # http_method_names = ["patch","delete"]
    queryset = Tweets.objects.filter(deleted=False).order_by("id")

    def destroy(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            product.deleted_at = datetime.utcnow()
            product.deleted = True
            product.save()
        except:
            return Response(
                {
                    "status": True,
                    "message": "Opps Some Error Occured Try Again",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {
                    "status": True,
                    "message": "Deleted SuccessFully",
                    "status_code": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )

    def create(self, request, *args, **kwargs):
        if len(request.data) != 0:
            try:
                response = super().create(request, *args, **kwargs)
            except Exception as e:
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
                        "message": "Tweet SuccessFully Done",
                        "status_code": status.HTTP_200_OK,
                        "tweet": response.data["tweet_serializer"],
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {
                    "status": False,
                    "message": {"content": "This field is required"},
                    "status_code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def partial_update(self, request, *args, **kwargs):
        try:
            res = super().partial_update(request, *args, **kwargs)
            serializer = TweetSerializer(data=res.data)
            if serializer.is_valid():
                print(serializer.data)
        except Exception as e:
            print(e)
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
                    "message": "Tweet SuccessFully Updated",
                    "status_code": status.HTTP_200_OK,
                    "data": res.data["tweet_serializer"]
                },
                status=status.HTTP_200_OK,
            )


class TweetDisplayView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]
    serializer_class = TweetDisplaySerializer
    queryset = Tweets.objects.filter(deleted=False).order_by("-id")

    def list(self, request):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "All Tweets SuccessFully Retreived",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# class UserDetails(viewsets.ModelViewSet):
# permission_classes = (IsAuthenticated,)
# http_method_names = ["get"]


class TopTweetDisplayView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]
    serializer_class = TweetDisplaySerializer
    queryset = (
        Tweets.objects.filter(deleted=False).annotate(
            total=Count("tweet_like", distinct=True)
            + Count("tweet_comment", distinct=True)
        )
    ).order_by("-total")[:5]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "All Tweets SuccessFully Retreived",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
