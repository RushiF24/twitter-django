from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import FollowSerializer, FollowingsSerializer, FollowersSerializer
from .models import Follow
from notification.models import Notification
# Create your views here.

User = get_user_model()

class FollowUserView(generics.CreateAPIView):
    # queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )

   

    def get_serializer(self, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            kwargs.setdefault('context', self.get_serializer_context())
            serializer = serializer_class(*args, **kwargs)
            user = self.request.user
            following_ls = user.following.values_list('following_id', flat=True) #gives list containing tuples if flat set to False
            serializer.fields['following'].queryset = User.objects.exclude(pk=user.pk).exclude(id__in=following_ls)
            return serializer
        except Exception as e:
            raise serializer.ValidationError("You already followed")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        following = get_object_or_404(User,username=self.request.data['following'])

        if not serializer.is_valid():
            raise ValidationError({"detail": "You are already following the user"})
        
        serializer.save(following=following, follower=self.request.user) 
        headers = self.get_success_headers(serializer.data)

        Notification.objects.create(message=f"{self.request.user} followed you", user=following)
        # notification = Notification.objects.create(message=f"{self.request.user} followed you", user=following)
        # notification.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UnFollowUserView(generics.DestroyAPIView):    
    serializer_class = FollowSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        following = User.objects.get(username=self.kwargs['username'])
        return get_object_or_404(Follow, follower=self.request.user, following=following)

class ListFollowerUserView(generics.ListAPIView):
    serializer_class = FollowersSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,  )

    def get_queryset(self):
        if 'username' in self.kwargs:
            following = User.objects.get(username=self.kwargs['username'])
        else:
            following = self.request.user 
        return Follow.objects.filter(following=following)

class ListFollowingUserView(generics.ListAPIView):
    serializer_class = FollowingsSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        if 'username' in self.kwargs:
            follower = User.objects.get(username=self.kwargs['username'])
        else:
            follower = self.request.user 
        return Follow.objects.filter(follower=follower)