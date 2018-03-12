import stripe
import calendar,datetime
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.template import loader
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import render , redirect
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from creditcard.models import Card
from creditcard.forms import CardForm


# view to show all credit cards for client
class CreditcardPageView(View) :

    def get(self, request, client_id):
        response = {'client_id':client_id}
        response['cards'] = Card.objects.filter(client_id=client_id)
        return render(request,'creditcard/creditcard.html', response )

 
#view to create credit card for client
class CreateCreditCardPageView(View):
    
    def get(self, request, client_id):
        response = {'client_id': client_id }
        response['form'] = CardForm()
        return render(request, 'creditcard/createcreditcard.html', response)
    
    def post(self, request, client_id):
        response = {'client_id': client_id }
        response['form'] = CardForm()
        form = CardForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            card = Card.objects.filter(client_id=client_id)
            if card :
            	pass
            else :
                f.primary=True
            f.expirydate=request.POST.get('expirydate')
            client=User.objects.get(id=client_id)
            f.client = client 
            f.card_holder = client.get_full_name()
            stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
            customer = stripe.Customer.retrieve(client.stripetoken)
            cardtoken=customer.sources.create(source="tok_mastercard")
            f.card_token=cardtoken['id']
            client.save()
            f.save()
            return redirect(reverse('creditcard' ,kwargs ={'client_id': client_id}))
        else:
        	return render(request, 'creditcard/createcreditcard.html', response)


# view to delete credit card for client
class DeleteCreditCardPageView(View):

    def get(self, request, client_id, card_id):
        card = Card.objects.get(id=card_id)
        stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
        cu = stripe.Customer.retrieve(card.client.stripetoken)
        cu.sources.retrieve(card.card_token).delete()
        Card.objects.filter(id=card_id).delete()
        return redirect(reverse('creditcard' ,kwargs ={'client_id': client_id}))


#view  to make primary credit card
class PrimaryCreditCardPageView(View):

    def get(self, request, client_id, card_id):
        Card.objects.filter(client_id=client_id).update(primary=False)
        Card.objects.filter(id=card_id).update(primary=True)
        return redirect(reverse('creditcard' ,kwargs ={'client_id': client_id}))

primary_creditcard_page_view = PrimaryCreditCardPageView.as_view()