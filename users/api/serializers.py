from users.models import User
from rest_framework import serializers

#serializer of user model 
class UserSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = User
        fields = ('id', 'email', 'get_full_name', 'role' ,'owner')
