from creditcard.models import Card
from rest_framework import serializers

# serializer class for card model
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CreateCreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('card_number','cvv_number','expirydate','client')