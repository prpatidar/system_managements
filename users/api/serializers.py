from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password')

class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
   
    class Meta:
    	model = User
        fields = ('current_password', 'new_password')