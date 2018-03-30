import stripe

from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from creditcard.models import Card
from users.models import User
from creditcard.api.serializers import CardSerializer , CreateCreditCardSerializer


# view to list clients credit card in api view 
class ClientCreditCardsView(generics.ListAPIView):
    
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get(self, request):
        try:
            client = User.objects.get(email=request.user)
            if client.role == 'client':
                queryset = Card.objects.filter(client_id=client.id)
                serializer = CardSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'status': False,'message': 'you are not a Authorized client '},
                                status=status.HTTP_400_BAD_REQUEST) 
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "First Login as a client"},
                            status=status.HTTP_400_BAD_REQUEST)

class CreateCreditCardApiView(generics.CreateAPIView):
    serializer_class = CreateCreditCardSerializer

    def post(self,request):
        data=request.data
        primary = False
        try:
            client = User.objects.get(email=request.user)
            if client.role != 'client':
                return Response({'status': False,'message': 'you are not a Authorized client to Add credit card'},
                                status=status.HTTP_400_BAD_REQUEST) 
        # import pdb; pdb.set_trace()
            if client :
                pass
            else :
                primary = True
            mutable = data._mutable
            data._mutable = True
            data['client'] = client.pk
            data._mutable = mutable
            card_serializer = CreateCreditCardSerializer(data=data,context={'request': request})
            if card_serializer.is_valid(raise_exception=True):
                card_serializer.save()
                card = Card.objects.get(card_number=data['card_number'],cvv_number=data['cvv_number'],expirydate=data['expirydate'])
                card.card_holder = client.get_full_name()
                stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
                customer = stripe.Customer.retrieve(client.stripetoken)
                cardtoken=customer.sources.create(source="tok_mastercard")
                card.card_token=cardtoken['id']
                card.primary = primary
                card.save()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'status': False,'message': 'Error Occured'},
                                status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "First Login to Create Credit Card"},
                            status=status.HTTP_400_BAD_REQUEST)
        

class CreditCardsView(generics.ListAPIView):
    
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get(self, request):
        try:
            client = User.objects.get(email=request.user.email)
            queryset = Card.objects.filter(client_id=client.id)
            serializer = CardSerializer(queryset, many=True)
            return Response(serializer.data)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "First Login "},
                            status=status.HTTP_400_BAD_REQUEST)
        

class CreditCardView(generics.ListAPIView):
    
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get(self, request,card_id):
        try:
            client = User.objects.get(email=request.user.email)
            Card.objects.filter(client_id=client.id).update(primary=False)
            card = Card.objects.filter(client_id=client.id,id=card_id).update(primary=True)
            queryset = Card.objects.filter(id=card_id)
            serializer = CardSerializer(queryset, many=True)
            return Response(serializer.data)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "First Login "},
                            status=status.HTTP_400_BAD_REQUEST)

class DeleteCreditCardView(generics.ListAPIView):
    
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get(self, request,card_id):
        try:
            card = Card.objects.get(id=card_id)
            if card.primary == True :
                return Response({'status': False,
                             'message': "make a one primary card before deletion of a primary card  "},
                            status=status.HTTP_400_BAD_REQUEST)
            Card.objects.filter(id=card_id).delete()
            return Response({'status': True,
                             'message': "deleted successfully  "},
                            status=status.HTTP_200_OK)
            
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "First Login "},
                            status=status.HTTP_400_BAD_REQUEST)