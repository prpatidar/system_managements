from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'password')

class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username','first_name', 'last_name', 'email', 'password','role','createdby')

class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username','first_name', 'last_name', 'email', 'password','role','createdby','stripetoken')


class EditEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'password',)

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

class ForgetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ('email',)