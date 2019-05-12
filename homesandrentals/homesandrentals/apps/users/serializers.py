from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
import re
import json


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'email': {'write_only': True},
                        'password': {'write_only': True}, }
        fields = ('username', 'email', 'phone', 'password', 'isActive',)

    def validate_username(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError(
                'Please provide a correct username.')

        return value

    def validate_email(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError(
                'please provide a correct email.')

        if not re.match(r"[a-zA-z0-9\.]+@[a-z]+\.[a-z]+", value):
            raise serializers.ValidationError('please provide a valid email.')

        return value

    def validate_phone(self, value):
        if len(value) < 12:
            raise serializers.ValidationError(
                'please provide a correct phone number (Include the zip code).')

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'please provide a password of not less than 8 characters.')

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'no such user with this email and password.')

        if not user.isActive:
            raise serializers.ValidationError('user account is deactivated.')

        return {
            'username': user.username,
            'token': user.token,
        }
