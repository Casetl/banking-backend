from rest_framework import serializers
from .models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address']