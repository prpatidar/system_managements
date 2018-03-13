from users.models import User
from rest_framework import serializers

#serializer of user model 
# class UserSerializer(serializers.ModelSerializer):
    
#     owner = serializers.ReadOnlyField(source='owner.email')

#     class Meta:
#         model = User
#         fields = ('id', 'email', 'get_full_name', 'role' ,'owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
