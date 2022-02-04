from django.http import HttpResponse
from .models import Commission, Project
from django.contrib.auth.models import User

import time
class StripeWebhook_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        return HttpResponse(content=f'Unhandled Webhook received: {event["type"]}', status=200) 

    def handle_payment_intent_succeeded(self, event):
        #if payment successful then add to database if the payment not already in the database
        intent = event.data.object
        pid = intent.id
        user = User.objects.get(id=intent.metadata.user)
        item = Project.objects.get(id=intent.metadata.item)

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        comm_exists = False 
        attempt = 1
        #5 second delay repeat check when adding to avoid any duplicate problems
        while attempt <= 5:
            try:
                commission = Commission.objects.get(
                    full_name__iexact=shipping_details.name, 
                    email__iexact=shipping_details.name, 
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country, 
                    postcode__iexact=shipping_details.address.postal_code, 
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state, 
                    commItem=item,
                    user=user,
                    stripe_pid=pid
                ) 
                comm_exists = True
                break 
            except Commission.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if comm_exists:
            #respond OK to stripe but dont add anything to database
            return HttpResponse(content=f'Webhook received: {event["type"]} | Order already in database', status=200)
        else:
            commission = None
            try:
                commission = Commission.objects.create(
                    full_name=shipping_details.name, 
                    email=shipping_details.name, 
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country, 
                    postcode=shipping_details.address.postal_code, 
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    commItem=item,
                    user=user,
                    stripe_pid=pid
                )
            except Exception as e:
                #if adding failed in any way, cancel, delete and tell stripe it failed and retry later
                if commission:
                    commission.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR {e}', status=500)
        return HttpResponse(content=f'Webhook received: {event["type"]} | SUCCESS order added to database', status=200) 

    def handle_payment_intent_failed(self, event):
        return HttpResponse(content=f'Webhook received: {event["type"]}', status=200)