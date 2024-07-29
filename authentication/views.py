from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, status
from authentication.serializers import RegisterSerializer, MyTokenObtainPairSerializer, UserProfileSerializer, UserSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
from .models import UserProfile, PasswordReset
from .permissions import IsOwner

import os
User = get_user_model()
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewset(ModelViewSet):

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user

        # if user.is_staff:
        #     return User.objects.all()
        # return User.objects.filter(id=user.id)
        # .annotate(
        #     followers=Count('follower', distinct=True),
        #     followings=Count('following',  distinct=True)
        # )
        return User.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopUsersView(generics.ListAPIView):
    # queryset = User.objects.filter(is_active=True).annotate(
    #     followers=Count('follower')
    # ).order_by("-followers")[:5]

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        # gives list containing tuples if flat set to False
        following_ls = user.following.values_list('following_id', flat=True)
        return User.objects.filter(is_active=True).exclude(pk=user.pk).exclude(id__in=following_ls).annotate(
            followers=Count('follower')
        ).order_by("-followers")[:8]


class ResetPasswordRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        email = data["email"]
        user = User.objects.filter(email__iexact=email).first()
        print(user)

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            print(token)
            reset.save()

            # reset_url
            return Response({'success': 'We have sent you a link to reset your password', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            return Response({'error': 'password do not match'}, status=status.HTTP_400_BAD_REQUEST)

        reset_obj = PasswordReset.objects.filter(token=token).first()
        print(reset_obj)

        if reset_obj is None:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=reset_obj.email)

        if user:
            user.set_password(new_password)
            user.save()

            reset_obj.delete()

            return Response({'success': 'password changed succesfully'})
        else:
            return Response({'error': 'usern not found'}, status=status.HTTP_404_NOT_FOUND)
