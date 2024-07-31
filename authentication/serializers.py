from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import AbstractBaseUser, update_last_login
from rest_framework_simplejwt.settings import api_settings
from .models import UserProfile
from follow.models import Follow
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, required=True, write_only=True)

    confirm_password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('password not matched')
        return attrs

    def create(self, validated_data):
        print(validated_data)
        # validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create( 
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        print("this is data", data)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if hasattr(self.user, 'profile'):
            image = str(self.user.profile.image)
        else:
            image = None
            
        data["user"] = {'email': self.user.email, 'id': self.user.id, 'image':image}
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

class UserProfileSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=False)
    banner_image = serializers.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ('id', 'image', 'banner_image', 'bio', 'birth_date', 'location')

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    profile = UserProfileSerializer(many=False)

    followers = serializers.SerializerMethodField('get_followers_count')
    followings = serializers.SerializerMethodField('get_followings_count')
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'profile', 'followers', 'followings')
        # depth = 1

    
    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_followings_count(self, obj):
        return Follow.objects.filter(follower=obj).count()
        
    

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        if profile_data:
            user = User.objects.create(**validated_data)
            profile = UserProfile.objects.create(user=user , **profile_data)

        return user
    

    def update(self, instance, validated_data):
        print(validated_data, instance, type(instance))
        profile_data = validated_data.pop('profile', None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        instance.save()

        if profile_data:
            # print(profile_data)
            profile, created = UserProfile.objects.get_or_create(user=instance)
            profile.image = profile_data.get('image', profile.image)
            profile.banner_image = profile_data.get('banner_image', profile.banner_image)
            profile.bio = profile_data.get('bio', profile.bio)
            profile.birth_date = profile_data.get('birth_date', profile.birth_date)
            profile.location = profile_data.get('location', profile.location)
            profile.save()

        return instance

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, required=True, write_only=True)

    confirm_password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, required=True, write_only=True)