from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'role', 'is_verified']

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)