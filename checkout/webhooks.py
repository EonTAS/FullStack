from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWebhook_Handler

import stripe
# stripe webhook demo code
@require_POST
@csrf_exempt
def webhook(request):    
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']

    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        print('Unhandled event type {}'.format(event['type']))
        return HttpResponse(content=e, status=400)
    print("success")
    return HttpResponse(status=200)