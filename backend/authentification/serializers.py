# backend/authentification/serializers.py
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'can_add']


class LeaderboardSerializer(serializers.ModelSerializer):
    prompt_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['email', 'prompt_count']
