from creditcard.models import Card
from rest_framework import viewsets
from creditcard.api.serializers import CardSerializer
from rest_framework import generics
from rest_framework.response import Response


class ClientCreditCardsView(generics.ListCreateAPIView):
    
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get(self, request,client_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Card.objects.filter(client_id=client_id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)

client_creditcards_page_view = ClientCreditCardsView.as_view()
