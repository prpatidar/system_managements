from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from creditcard.models import Card
from creditcard.api.serializers import CardSerializer


# view to list clients credit card in api view 
class ClientCreditCardsView(generics.ListCreateAPIView):
    
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get(self, request,client_id):
        queryset = Card.objects.filter(client_id=client_id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)

